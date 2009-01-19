from weakref import WeakKeyDictionary



class LazyValue(object):
    """Marker to be used as a base class on lazily evaluated values."""



class Expr(LazyValue):
    pass

class Compile(object):
    """Compiler based on the concept of generic functions."""

    def __init__(self, parent=None):
        self._local_dispatch_table = {}
        self._local_precedence = {}
        self._local_reserved_words = {}
        self._dispatch_table = {}
        self._precedence = {}
        self._reserved_words = {}
        self._hash = None
        self._children = WeakKeyDictionary()
        self._parents = []
        if parent:
            self._parents.extend(parent._parents)
            self._parents.append(parent)
            parent._children[self] = True
            self._update_cache()

    def _update_cache(self):
        for parent in self._parents:
            self._dispatch_table.update(parent._local_dispatch_table)
            self._precedence.update(parent._local_precedence)
            self._reserved_words.update(parent._local_reserved_words)
        self._dispatch_table.update(self._local_dispatch_table)
        self._precedence.update(self._local_precedence)
        self._reserved_words.update(self._local_reserved_words)
        for child in self._children:
            child._update_cache()

    def add_reserved_words(self, words):
        """Include words to be considered reserved and thus escaped.

        Reserved words are escaped during compilation when they're
        seen in a SQLToken expression.
        """
        self._local_reserved_words.update((word.lower(), True)
                                          for word in words)
        self._update_cache()

    def remove_reserved_words(self, words):
        self._local_reserved_words.update((word.lower(), None)
                                          for word in words)
        self._update_cache()

    def is_reserved_word(self, word):
        return self._reserved_words.get(word.lower()) is not None

    def create_child(self):
        """Create a new instance of L{Compile} which inherits from this one.

        This is most commonly used to customize a compiler for
        database-specific compilation strategies.
        """
        return self.__class__(self)

    def when(self, *types):
        def decorator(method):
            for type in types:
                self._local_dispatch_table[type] = method
            self._update_cache()
            return method
        return decorator

    def get_precedence(self, type):
        return self._precedence.get(type, MAX_PRECEDENCE)

    def set_precedence(self, precedence, *types):
        for type in types:
            self._local_precedence[type] = precedence
        self._update_cache()

    def _compile_single(self, expr, state, outer_precedence):
        # FASTPATH This method is part of the fast path.  Be careful when
        #          changing it (try to profile any changes).

        cls = expr.__class__
        dispatch_table = self._dispatch_table
        if cls in dispatch_table:
            handler = dispatch_table[cls]
        else:
            for mro_cls in cls.__mro__:
                # First iteration will always fail because we've already
                # tested that the class itself isn't in the dispatch table.
                if mro_cls in dispatch_table:
                    handler = dispatch_table[mro_cls]
                    break
            else:
                raise CompileError("Don't know how to compile type %r of %r"
                                   % (expr.__class__, expr))
        inner_precedence = state.precedence = \
                           self._precedence.get(cls, MAX_PRECEDENCE)
        statement = handler(self, expr, state)
        if inner_precedence < outer_precedence:
            return "(%s)" % statement
        return statement

    def __call__(self, expr, state=None, join=", ", raw=False, token=False):
        """Compile the given expression into a SQL statement.

        @param expr: The expression to compile.
        @param state: An instance of State, or None, in which case it's
            created internally (and thus can't be accessed).
        @param join: The string token to use to put between
            subexpressions. Defaults to ", ".
        @param raw: If true, any string or unicode expression or
            subexpression will not be further compiled.
        @param token: If true, any string or unicode expression will
            be considered as a SQLToken, and quoted properly.
        """
        # FASTPATH This method is part of the fast path.  Be careful when
        #          changing it (try to profile any changes).

        expr_type = type(expr)

        if (expr_type is SQLRaw or
            raw and (expr_type is str or expr_type is unicode)):
            return expr

        if token and (expr_type is str or expr_type is unicode):
            expr = SQLToken(expr)

        if state is None:
            state = State()

        outer_precedence = state.precedence
        if expr_type is tuple or expr_type is list:
            compiled = []
            for subexpr in expr:
                subexpr_type = type(subexpr)
                if subexpr_type is SQLRaw or raw and (subexpr_type is str or
                                                      subexpr_type is unicode):
                    statement = subexpr
                elif subexpr_type is tuple or subexpr_type is list:
                    state.precedence = outer_precedence
                    statement = self(subexpr, state, join, raw)
                else:
                    if token and (subexpr_type is unicode or
                                  subexpr_type is str):
                        subexpr = SQLToken(subexpr)
                    statement = self._compile_single(subexpr, state,
                                                     outer_precedence)
                compiled.append(statement)
            statement = join.join(compiled)
        else:
            statement = self._compile_single(expr, state, outer_precedence)
        state.precedence = outer_precedence

        return statement


class CompilePython(Compile):

    def get_matcher(self, expr):
        exec "def match(get_column): return bool(%s)" % self(expr)
        return match


class State(object):
    """All the data necessary during compilation of an expression.

    @ivar aliases: Dict of L{Column} instances to L{Alias} instances,
        specifying how columns should be compiled as aliases in very
        specific situations.  This is typically used to work around
        strange deficiencies in various databases.

    @ivar auto_tables: The list of all implicitly-used tables.  e.g.,
        in store.find(Foo, Foo.attr==Bar.id), the tables of Bar and
        Foo are implicitly used because columns in them are
        referenced. This is used when building tables.

    @ivar join_tables: If not None, when Join expressions are
        compiled, tables seen will be added to this set. This acts as
        a blacklist against auto_tables when compiling Joins, because
        the generated statements should not refer to the table twice.

    @ivar context: an instance of L{Context}, specifying the context
        of the expression currently being compiled.

    @ivar precedence: Current precedence, automatically set and restored
        by the compiler. If an inner precedence is lower than an outer
        precedence, parenthesis around the inner expression are
        automatically emitted.
    """

    def __init__(self):
        self._stack = []
        self.precedence = 0
        self.parameters = []
        self.auto_tables = []
        self.join_tables = None
        self.context = None
        self.aliases = None

    def push(self, attr, new_value=Undef):
        """Set an attribute in a way that can later be reverted with L{pop}.
        """
        old_value = getattr(self, attr, None)
        self._stack.append((attr, old_value))
        if new_value is Undef:
            new_value = copy(old_value)
        setattr(self, attr, new_value)
        return old_value

    def pop(self):
        """Revert the topmost L{push}.
        """
        setattr(self, *self._stack.pop(-1))


compile = Compile()
compile_python = CompilePython()

@compile_python.when(Expr)
def compile_python_unsupported(compile, expr, state):
    raise CompileError("Can't compile python expressions with %r" % type(expr))


class Comparable(object):

    def __eq__(self, other):
        if other is not None and not isinstance(other, (Expr, Variable)):
            other = getattr(self, "variable_factory", Variable)(value=other)
        return Eq(self, other)

    def __ne__(self, other):
        if other is not None and not isinstance(other, (Expr, Variable)):
            other = getattr(self, "variable_factory", Variable)(value=other)
        return Ne(self, other)

    def __gt__(self, other):
        if not isinstance(other, (Expr, Variable)):
            other = getattr(self, "variable_factory", Variable)(value=other)
        return Gt(self, other)

    def __ge__(self, other):
        if not isinstance(other, (Expr, Variable)):
            other = getattr(self, "variable_factory", Variable)(value=other)
        return Ge(self, other)

    def __lt__(self, other):
        if not isinstance(other, (Expr, Variable)):
            other = getattr(self, "variable_factory", Variable)(value=other)
        return Lt(self, other)

    def __le__(self, other):
        if not isinstance(other, (Expr, Variable)):
            other = getattr(self, "variable_factory", Variable)(value=other)
        return Le(self, other)

    def __rshift__(self, other):
        if not isinstance(other, (Expr, Variable)):
            other = getattr(self, "variable_factory", Variable)(value=other)
        return RShift(self, other)

    def __lshift__(self, other):
        if not isinstance(other, (Expr, Variable)):
            other = getattr(self, "variable_factory", Variable)(value=other)
        return LShift(self, other)

    def __and__(self, other):
        if not isinstance(other, (Expr, Variable)):
            other = getattr(self, "variable_factory", Variable)(value=other)
        return And(self, other)

    def __or__(self, other):
        if not isinstance(other, (Expr, Variable)):
            other = getattr(self, "variable_factory", Variable)(value=other)
        return Or(self, other)

    def __add__(self, other):
        if not isinstance(other, (Expr, Variable)):
            other = getattr(self, "variable_factory", Variable)(value=other)
        return Add(self, other)

    def __sub__(self, other):
        if not isinstance(other, (Expr, Variable)):
            other = getattr(self, "variable_factory", Variable)(value=other)
        return Sub(self, other)

    def __mul__(self, other):
        if not isinstance(other, (Expr, Variable)):
            other = getattr(self, "variable_factory", Variable)(value=other)
        return Mul(self, other)

    def __div__(self, other):
        if not isinstance(other, (Expr, Variable)):
            other = getattr(self, "variable_factory", Variable)(value=other)
        return Div(self, other)

    def __mod__(self, other):
        if not isinstance(other, (Expr, Variable)):
            other = getattr(self, "variable_factory", Variable)(value=other)
        return Mod(self, other)

    def is_in(self, others):
        if not isinstance(others, Expr):
            if not others:
                return None
            others = list(others)
            variable_factory = getattr(self, "variable_factory", Variable)
            for i, other in enumerate(others):
                if not isinstance(other, (Expr, Variable)):
                    others[i] = variable_factory(value=other)
        return In(self, others)

    def like(self, other, escape=Undef, case_sensitive=None):
        if not isinstance(other, (Expr, Variable)):
            other = getattr(self, "variable_factory", Variable)(value=other)
        return Like(self, other, escape, case_sensitive)

    def lower(self):
        return Lower(self)

    def upper(self):
        return Upper(self)

class ComparableExpr(Expr, Comparable):
    pass

class BinaryExpr(ComparableExpr):

    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

class CompoundExpr(ComparableExpr):

    def __init__(self, *exprs):
        self.exprs = exprs

class BinaryOper(BinaryExpr):
    oper = " (unknown) "

class NonAssocBinaryOper(BinaryOper):
    oper = " (unknown) "

class CompoundOper(CompoundExpr):
    oper = " (unknown) "

class Eq(BinaryOper):
    oper = " = "

class Ne(BinaryOper):
    oper = " != "

class Add(CompoundOper):
    oper = "+"

class Sub(NonAssocBinaryOper):
    oper = "-"

class Mul(CompoundOper):
    oper = "*"

class Div(NonAssocBinaryOper):
    oper = "/"

class Mod(NonAssocBinaryOper):
    oper = "%"


class And(CompoundOper):
    oper = " AND "

class Or(CompoundOper):
    oper = " OR "