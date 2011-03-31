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
        vs = node.values
        vs = [self.visit(n) for n in vs]
        return ast.Call(func=f, args = vs, keywords=[])


converter = ConvertAndToLogicalAndCall()


def parse(expr, context):
    'parse a filter expression and create syntax tree of the expression'
    a = ast.parse(expr, mode='eval')
    # print ast.dump(a)
    a1 = converter.visit(a)
    a2 = ast.fix_missing_locations(a1)
    # print ast.dump(a2)
    code = compile(a2, '<unknown>', 'eval')
    from _logical_calls import calls
    e = calls.copy()
    e.update(context)
    return eval(code, e)


def test():
    from expression import measure
    a = measure('a')
    b = measure('b')
    env = {'a':a, 'b': b}
    print parse("a==3 and b==4", env)

    c = measure('c')
    env['c'] = c
    print parse('a==3 and b==4 and c==5', env)

    print parse('a==3 and b==4 or c==5', env)
    return


def main():
    test()
    return


if __name__=='__main__': main()


# version
__id__ = "$Id$"

# End of file 
