from weakref import WeakKeyDictionary
from copy import copy
from vnf.components import Undef
from vnf.variables import (
    Variable, RawStrVariable, UnicodeVariable, LazyValue,
    DateTimeVariable, DateVariable, TimeVariable, TimeDeltaVariable,
    BoolVariable, IntVariable, FloatVariable, DecimalVariable)
from vnf.components.exceptions import CompileError, NoTableError, ExprError



# --------------------------------------------------------------------
# Base classes 

MAX_PRECEDENCE = 1000

class Expr(LazyValue):
    pass

# Basic compiler infrastructure

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
                raise Exception("Don't know how to compile type %r of %r"
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
    raise Exception("Can't compile python expressions with %r" % type(expr))

# Base classes for expressions

MAX_PRECEDENCE = 1000

class Expr(LazyValue):
    __slots__ = ()

@compile_python.when(Expr)
def compile_python_unsupported(compile, expr, state):
    raise CompileError("Can't compile python expressions with %r" % type(expr))


class Comparable(object):
    __slots__ = ()

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
            others = list(others)
            if not others:
                return False
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
    __slots__ = ()

class BinaryExpr(ComparableExpr):
    __slots__ = ("expr1", "expr2")

    def __init__(self, expr1, expr2):
        self.expr1 = expr1
        self.expr2 = expr2

class CompoundExpr(ComparableExpr):
    __slots__ = ("exprs",)

    def __init__(self, *exprs):
        self.exprs = exprs

# --------------------------------------------------------------------
# Operators

class BinaryOper(BinaryExpr):
    __slots__ = ()
    oper = " (unknown) "

@compile.when(BinaryOper)
@compile_python.when(BinaryOper)
def compile_binary_oper(compile, expr, state):
    return "%s%s%s" % (compile(expr.expr1, state), expr.oper,
                       compile(expr.expr2, state))


class NonAssocBinaryOper(BinaryOper):
    __slots__ = ()
    oper = " (unknown) "

@compile.when(NonAssocBinaryOper)
@compile_python.when(NonAssocBinaryOper)
def compile_non_assoc_binary_oper(compile, expr, state):
    expr1 = compile(expr.expr1, state)
    state.precedence += 0.5 # Enforce parentheses.
    expr2 = compile(expr.expr2, state)
    return "%s%s%s" % (expr1, expr.oper, expr2)


class CompoundOper(CompoundExpr):
    __slots__ = ()
    oper = " (unknown) "

@compile.when(CompoundOper)
def compile_compound_oper(compile, expr, state):
    return compile(expr.exprs, state, join=expr.oper)

@compile_python.when(CompoundOper)
def compile_compound_oper(compile, expr, state):
    return compile(expr.exprs, state, join=expr.oper.lower())


class Eq(BinaryOper):
    __slots__ = ()
    oper = " = "

@compile.when(Eq)
def compile_eq(compile, eq, state):
    if eq.expr2 is None:
        return "%s IS NULL" % compile(eq.expr1, state)
    return "%s = %s" % (compile(eq.expr1, state), compile(eq.expr2, state))

@compile_python.when(Eq)
def compile_eq(compile, eq, state):
    return "%s == %s" % (compile(eq.expr1, state), compile(eq.expr2, state))


class Ne(BinaryOper):
    __slots__ = ()
    oper = " != "

@compile.when(Ne)
def compile_ne(compile, ne, state):
    if ne.expr2 is None:
        return "%s IS NOT NULL" % compile(ne.expr1, state)
    return "%s != %s" % (compile(ne.expr1, state), compile(ne.expr2, state))


class Gt(BinaryOper):
    __slots__ = ()
    oper = " > "

class Ge(BinaryOper):
    __slots__ = ()
    oper = " >= "

class Lt(BinaryOper):
    __slots__ = ()
    oper = " < "

class Le(BinaryOper):
    __slots__ = ()
    oper = " <= "

class RShift(BinaryOper):
    __slots__ = ()
    oper = ">>"

class LShift(BinaryOper):
    __slots__ = ()
    oper = "<<"


class Like(BinaryOper):
    __slots__ = ("escape", "case_sensitive")
    oper = " LIKE "

    def __init__(self, expr1, expr2, escape=Undef, case_sensitive=None):
        self.expr1 = expr1
        self.expr2 = expr2
        self.escape = escape
        self.case_sensitive = case_sensitive

@compile.when(Like)
def compile_like(compile, like, state, oper=None):
    statement = "%s%s%s" % (compile(like.expr1, state), oper or like.oper,
                            compile(like.expr2, state))
    if like.escape is not Undef:
        statement = "%s ESCAPE %s" % (statement, compile(like.escape, state))
    return statement

# It's easy to support it. Later.
compile_python.when(Like)(compile_python_unsupported)


class In(BinaryOper):
    __slots__ = ()
    oper = " IN "

@compile.when(In)
def compile_in(compile, expr, state):
    expr1 = compile(expr.expr1, state)
    state.precedence = 0 # We're forcing parenthesis here.
    return "%s IN (%s)" % (expr1, compile(expr.expr2, state))

@compile_python.when(In)
def compile_in(compile, expr, state):
    expr1 = compile(expr.expr1, state)
    state.precedence = 0 # We're forcing parenthesis here.
    return "%s in (%s,)" % (expr1, compile(expr.expr2, state))


class Add(CompoundOper):
    __slots__ = ()
    oper = "+"

class Sub(NonAssocBinaryOper):
    __slots__ = ()
    oper = "-"

class Mul(CompoundOper):
    __slots__ = ()
    oper = "*"

class Div(NonAssocBinaryOper):
    __slots__ = ()
    oper = "/"

class Mod(NonAssocBinaryOper):
    __slots__ = ()
    oper = "%"


class And(CompoundOper):
    __slots__ = ()
    oper = " AND "

class Or(CompoundOper):
    __slots__ = ()
    oper = " OR "

@compile.when(And, Or)
def compile_compound_oper(compile, expr, state):
    return compile(expr.exprs, state, join=expr.oper, raw=True)



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
    
# --------------------------------------------------------------------
# Plain SQL expressions.

class SQLRaw(str):
    """Subtype to mark a string as something that shouldn't be compiled.

    This is handled internally by the compiler.
    """
    __slots__ = ()


class SQLToken(str):
    """Marker for strings that should be considered as a single SQL token.

    These strings will be quoted, when needed.
    """
    __slots__ = ()

is_safe_token = re.compile("^[a-zA-Z][a-zA-Z0-9_]*$").match

@compile.when(SQLToken)
def compile_sql_token(compile, expr, state):
    if is_safe_token(expr) and not compile.is_reserved_word(expr):
        return expr
    return '"%s"' % expr.replace('"', '""')

@compile_python.when(SQLToken)
def compile_python_sql_token(compile, expr, state):
    return expr


class SQL(ComparableExpr):
    __slots__ = ("expr", "params", "tables")

    def __init__(self, expr, params=Undef, tables=Undef):
        self.expr = expr
        self.params = params
        self.tables = tables

@compile.when(SQL)
def compile_sql(compile, expr, state):
    if expr.params is not Undef:
        if type(expr.params) not in (tuple, list):
            raise CompileError("Parameters should be a list or a tuple, "
                               "not %r" % type(expr.params))
        for param in expr.params:
            state.parameters.append(param)
    if expr.tables is not Undef:
        state.auto_tables.append(expr.tables)
    return expr.expr

