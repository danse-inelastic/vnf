# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import ast

class ConvertAndToLogicalAndCall(ast.NodeTransformer):


    def visit_BoolOp(self, node):
        f = ast.Name(id='logical_%s' % node.op.__class__.__name__.lower(), ctx=ast.Load())
        return ast.Call(func=f, args = node.values, keywords=[])


converter = ConvertAndToLogicalAndCall()


def logical_and(a, b):
    return a.__l_and__(b)
def logical_or(a, b):
    return a.__l_or__(b)

env = {
    'logical_and': logical_and,
    'logical_or': logical_or,
    }



def parse(expr, context):
    'parse a filter expression and create syntax tree of the expression'
    a = ast.parse(expr, mode='eval')
    a1 = converter.visit(a)
    a2 = ast.fix_missing_locations(a1)
    code = compile(a2, '<unknown>', 'eval')
    e = env.copy()
    e.update(context)
    return eval(code, e)


def test():
    from expression import measure
    a = measure('a')
    b = measure('b')
    env = {'a':a, 'b': b}
    print parse("a==3 and b==4", env)
    return


def main():
    test()
    return


if __name__=='__main__': main()


# version
__id__ = "$Id$"

# End of file 
