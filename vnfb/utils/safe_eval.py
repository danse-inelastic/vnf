#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# safe_eval
#
# modified from the recipe from Babar K Zafar.
# the following is his note:
#
#----------------------------------------------------------------------
# I, Babar K. Zafar, the author or of this code dedicate any and all
# copyright interest in this code to the public domain. I make this
# dedication for the benefit of the public at large and to the
# detriment of our heirs and successors. I intend this dedication to
# be an overt act of relinquishment in perpetuity of all present and
# future rights this code under copyright law.
#
# Version 0.1 / May 27 2006
#----------------------------------------------------------------------
#
# The main difference is that ast instead of compiler.ast is used.
#



import inspect, ast
import thread, time

#----------------------------------------------------------------------
# Module globals.
#----------------------------------------------------------------------

# Toggle module level debugging mode.
DEBUG = False

# List of all AST node classes in ast.py.
all_ast_nodes = \
    [name for (name, obj) in inspect.getmembers(ast)
     if inspect.isclass(obj) and issubclass(obj, ast.AST)]

# List of all builtin functions and types (ignoring exception classes).
import types
if type(__builtins__) == types.ModuleType:
    iterbuiltins = inspect.getmembers(__builtins__)
else:
    iterbuiltins = __builtins__.iteritems()
all_builtins = \
    [name for (name, obj) in iterbuiltins
     if inspect.isbuiltin(obj) or (inspect.isclass(obj) and \
                                   not issubclass(obj, Exception))]

#----------------------------------------------------------------------
# Utilties.
#----------------------------------------------------------------------

def classname(obj):
    return obj.__class__.__name__

def is_valid_ast_node(name):
    return name in all_ast_nodes

def is_valid_builtin(name):
    return name in all_builtins

def get_node_lineno(node):
    return (node.lineno) and node.lineno or 0
       
#----------------------------------------------------------------------
# Restricted AST nodes & builtins.
#----------------------------------------------------------------------

# Deny evaluation of code if the AST contain any of the following nodes:
unallowed_ast_nodes = [
#   'Add', 'And',
#   'Assert', 'Assign', 'Attribute',
    'AugAssign', 'AugLoad', 'AugStore',
#   'BinOp', 'BitAnd', 'BitOr', 'BitXor', 'BoolOp',
#   'Break', 'Call',
#   'ClassDef', 'Compare', 'Continue',
#   'Del', 'Delete',
#   'Dict', 'Div', 'Ellipsis', 'Eq',
#   'ExceptHandler',
    'Exec',
#   'Expr', 'Expression',
#   'ExtSlice', 'FloorDiv', 'For', 'FunctionDef', 'GeneratorExp', 'Global',
#    'Gt', 'GtE', 'If', 'IfExp',
    'Import', 'ImportFrom',
#   'In', 'Index',
#   'Interactive', 'Invert', 'Is', 'IsNot', 'LShift', 'Lambda', 'List',
#   'ListComp', 'Load', 'Lt', 'LtE', 'Mod', 'Module', 'Mult', 'Name',
#   'Not', 'NotEq', 'NotIn', 'Num', 'Or',
#   'Param', 'Pass', 'Pow', 'Print', 'PyCF_ONLY_AST', 'RShift',
    'Raise',
#   'Repr',
#   'Return', 'Slice', 'Store', 'Str', 'Sub', 'Subscript', 'Suite',
    'TryExcept', 'TryFinally',
#   'Tuple', 'UAdd', 'USub', 'UnaryOp', 'While', 'With', 'Yield',
]

# Deny evaluation of code if it tries to access any of the following builtins:
unallowed_builtins = [
    '__import__',
#   'abs', 'apply', 'basestring', 'bool', 'buffer',
#   'callable', 'chr', 'classmethod', 'cmp', 'coerce',
    'compile',
#   'complex',
    'delattr',
#   'dict',
    'dir',
#   'divmod', 'enumerate',
    'eval', 'execfile', 'file',
#   'filter', 'float', 'frozenset',
    'getattr', 'globals', 'hasattr',
#    'hash', 'hex', 'id',
    'input',
#   'int', 'intern', 'isinstance', 'issubclass', 'iter',
#   'len', 'list',
    'locals',
#   'long', 'map', 'max', 'min', 'object', 'oct',
    'open',
#   'ord', 'pow', 'property', 'range',
    'raw_input',
#   'reduce',
    'reload',
#   'repr', 'reversed', 'round', 'set',
    'setattr',
#   'slice', 'sorted', 'staticmethod',  'str', 'sum', 'super',
#   'tuple', 'type', 'unichr', 'unicode',
    'vars',
#    'xrange', 'zip'
]

for ast_name in unallowed_ast_nodes:
    assert(is_valid_ast_node(ast_name)), 'invalide ast node: %s' % (ast_name,)
for name in unallowed_builtins:
    assert(is_valid_builtin(name)), 'invalid builtin: %s' % (name,)

def is_unallowed_ast_node(kind):
    return kind in unallowed_ast_nodes

def is_unallowed_builtin(name):
    return name in unallowed_builtins

#----------------------------------------------------------------------
# Restricted attributes.
#----------------------------------------------------------------------

# In addition to these we deny access to all lowlevel attrs (__xxx__).
unallowed_attr = [
    'im_class', 'im_func', 'im_self',
    'func_code', 'func_defaults', 'func_globals', 'func_name',
    'tb_frame', 'tb_next',
    'f_back', 'f_builtins', 'f_code', 'f_exc_traceback',
    'f_exc_type', 'f_exc_value', 'f_globals', 'f_locals']

def is_unallowed_attr(name):
    return (name[:2] == '__' and name[-2:] == '__') or \
           (name in unallowed_attr)

#----------------------------------------------------------------------
# SafeEvalVisitor.
#----------------------------------------------------------------------

class SafeEvalError(object):
    """
    Base class for all which occur while walking the AST.

    Attributes:
      errmsg = short decription about the nature of the error
      lineno = line offset to where error occured in source code
    """
    def __init__(self, errmsg, lineno):
        self.errmsg, self.lineno = errmsg, lineno
    def __str__(self):
        return "line %d : %s" % (self.lineno, self.errmsg)

class SafeEvalASTNodeError(SafeEvalError):
    "Expression/statement in AST evaluates to a restricted AST node type."
    pass
class SafeEvalBuiltinError(SafeEvalError):
    "Expression/statement in tried to access a restricted builtin."
    pass
class SafeEvalAttrError(SafeEvalError):
    "Expression/statement in tried to access a restricted attribute."
    pass


class SafeEvalVisitor(ast.NodeVisitor):
    """
    Data-driven visitor which walks the AST for some code and makes
    sure it doesn't contain any expression/statements which are
    declared as restricted in 'unallowed_ast_nodes'. We'll also make
    sure that there aren't any attempts to access/lookup restricted
    builtin declared in 'unallowed_builtins'. By default we also won't
    allow access to lowlevel stuff which can be used to dynamically
    access non-local envrioments.

    Interface:
      walk(ast) = validate AST and return True if AST is 'safe'

    Attributes:
      errors = list of SafeEvalError if walk() returned False

    Implementation:
    
    The visitor will automatically generate methods for all of the
    available AST node types and redirect them to self.ok or self.fail
    reflecting the configuration in 'unallowed_ast_nodes'. While
    walking the AST we simply forward the validating step to each of
    node callbacks which take care of reporting errors.
    """

    def __init__(self, *args, **kwds):
        "Initialize visitor by generating callbacks for all AST node types."
        
        ast.NodeVisitor.__init__(self, *args, **kwds)
        
        self.errors = []
        for ast_name in all_ast_nodes:
            # Don't reset any overridden callbacks.
            if getattr(self, 'visit' + ast_name, None): continue
            if is_unallowed_ast_node(ast_name):
                setattr(self, 'visit' + ast_name, self.fail)
            else:
                setattr(self, 'visit' + ast_name, self.ok)

                
    def walk(self, ast):
        "Validate each node in AST and return True if AST is 'safe'."
        self.visit(ast)
        return self.errors == []

        
    def visit(self, node):
        "Recursively validate node and all of its children."
        if DEBUG: self.trace(node)
        return ast.NodeVisitor.visit(self, node)
    

    def visit_Name(self, node):
        "Disallow any attempts to access a restricted builtin/attr."
        name = node.id
        lineno = get_node_lineno(node)
        if is_unallowed_builtin(name):
            self.errors.append(SafeEvalBuiltinError( \
                "access to builtin '%s' is denied" % name, lineno))
        elif is_unallowed_attr(name):
            self.errors.append(SafeEvalAttrError( \
                "access to attribute '%s' is denied" % name, lineno))
               
    def visit_Attribute(self, node):
        "Disallow any attempts to access a restricted attribute."
        name = node.attr
        lineno = get_node_lineno(node)
        if is_unallowed_attr(name):
            self.errors.append(SafeEvalAttrError( \
                "access to attribute '%s' is denied" % name, lineno))
            
    def ok(self, node, *args):
        "Default callback for 'harmless' AST nodes."
        pass
    
    def fail(self, node, *args):
        "Default callback for unallowed AST nodes."
        lineno = get_node_lineno(node)
        self.errors.append(SafeEvalASTNodeError( \
            "execution of '%s' statements is denied" % classname(node),
            lineno))

    def trace(self, node):
        "Debugging utility for tracing the validation of AST nodes."
        print node
        for attr in dir(node):
            if attr[:2] != '__':
                print ' ' * 4, "%-15.15s" % attr, getattr(node, attr)

#----------------------------------------------------------------------
# Safe 'eval' replacement.
#----------------------------------------------------------------------

class SafeEvalException(Exception):
    "Base class for all safe-eval related errors."
    pass

class SafeEvalCodeException(SafeEvalException):
    """
    Exception class for reporting all errors which occured while
    validating AST for source code in safe_eval().

    Attributes:
      code   = raw source code which failed to validate
      errors = list of SafeEvalError
    """
    def __init__(self, code, errors):
        self.code, self.errors = code, errors
    def __str__(self):
        return '\n'.join([str(err) for err in self.errors])

class SafeEvalContextException(SafeEvalException):
    """
    Exception class for reporting unallowed objects found in the dict
    intended to be used as the local enviroment in safe_eval().

    Attributes:
      keys   = list of keys of the unallowed objects
      errors = list of strings describing the nature of the error
               for each key in 'keys'
    """
    def __init__(self, keys, errors):
        self.keys, self.errors = keys, errors
    def __str__(self):
        return '\n'.join([str(err) for err in self.errors])
        
class SafeEvalTimeoutException(SafeEvalException):
    """
    Exception class for reporting that code evaluation execeeded
    the given timelimit.

    Attributes:
      timeout = time limit in seconds
    """
    def __init__(self, timeout):
        self.timeout = timeout
    def __str__(self):
        return "Timeout limit execeeded (%s secs) during exec" % self.timeout

def exec_timed(code, context, timeout_secs):
    """
    Dynamically execute 'code' using 'context' as the global enviroment.
    SafeEvalTimeoutException is raised if execution does not finish within
    the given timelimit.
    """
    assert(timeout_secs > 0)

    signal_finished = False
    
    def alarm(secs):
        def wait(secs):
            for n in xrange(timeout_secs):
                time.sleep(1)
                if signal_finished: break
            else:
                thread.interrupt_main()
        thread.start_new_thread(wait, (secs,))

    try:
        alarm(timeout_secs)
        exec code in context
        signal_finished = True
    except KeyboardInterrupt:
        raise SafeEvalTimeoutException(timeout_secs)

def safe_eval(code, context = {}, timeout_secs = 5, check_only=False):
    """
    Validate source code and make sure it contains no unauthorized
    expression/statements as configured via 'unallowed_ast_nodes' and
    'unallowed_builtins'. By default this means that code is not
    allowed import modules or access dangerous builtins like 'open' or
    'eval'. If code is considered 'safe' it will be executed via
    'exec' using 'context' as the global environment. More details on
    how code is executed can be found in the Python Reference Manual
    section 6.14 (ignore the remark on '__builtins__'). The 'context'
    enviroment is also validated and is not allowed to contain modules
    or builtins. The following exception will be raised on errors:

      if 'context' contains unallowed objects = 
        SafeEvalContextException

      if code is didn't validate and is considered 'unsafe' = 
        SafeEvalCodeException

      if code did not execute within the given timelimit =
        SafeEvalTimeoutException

    check_only: if check_only is true, only check whether the expression is safe.
    """   
    ctx_errkeys, ctx_errors = [], []
    for (key, obj) in context.items():
        if inspect.isbuiltin(obj):
            ctx_errkeys.append(key)
            ctx_errors.append("key '%s' : unallowed builtin %s" % (key, obj))
        if inspect.ismodule(obj):
            ctx_errkeys.append(key)
            ctx_errors.append("key '%s' : unallowed module %s" % (key, obj))

    if ctx_errors:
        raise SafeEvalContextException(ctx_errkeys, ctx_errors)

    ast1 = ast.parse(code)
    checker = SafeEvalVisitor()

    if checker.walk(ast1):
        if not check_only:
            exec_timed(code, context, timeout_secs)
    else:
        raise SafeEvalCodeException(code, checker.errors)
       
#----------------------------------------------------------------------
# Basic tests.
#----------------------------------------------------------------------

import unittest

class TestSafeEval(unittest.TestCase):
    def test_builtin(self):
        # attempt to access a unsafe builtin
        self.assertRaises(SafeEvalException,
            safe_eval, "open('test.txt', 'w')")

    def test_getattr(self):
        # attempt to get arround direct attr access
        self.assertRaises(SafeEvalException, \
            safe_eval, "getattr(int, '__abs__')")

    def test_func_globals(self):
        # attempt to access global enviroment where fun was defined
        self.assertRaises(SafeEvalException, \
            safe_eval, "def x(): pass; print x.func_globals")

    def test_lowlevel(self):
        # lowlevel tricks to access 'object'
        self.assertRaises(SafeEvalException, \
            safe_eval, "().__class__.mro()[1].__subclasses__()")

    def test_timeout_ok(self):
        # attempt to exectute 'slow' code which finishes within timelimit
        def test(): time.sleep(2)
        env = {'test':test}
        safe_eval("test()", env, timeout_secs = 5)

    def test_timeout_exceed(self):
        # attempt to exectute code which never teminates
        self.assertRaises(SafeEvalException, \
            safe_eval, "while 1: pass")

    def test_invalid_context(self):
        # can't pass an enviroment with modules or builtins
        env = {'f' : __builtins__.open, 'g' : time}
        self.assertRaises(SafeEvalException, \
            safe_eval, "print 1", env)

    def test_callback(self):
        # modify local variable via callback
        self.value = 0
        def test(): self.value = 1
        env = {'test':test}
        safe_eval("test()", env)
        self.assertEqual(self.value, 1)

if __name__ == "__main__":
    unittest.main()


# version
__id__ = "$Id$"

# End of file 
