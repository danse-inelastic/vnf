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


# this only works for python 2.5


import compiler.ast as ast
import compiler



# base class of visitors of ast node
class NodeVisitor(object):

    def visitNode(self, node):
        h = 'on%s' % node.__class__.__name__
        if hasattr(self, h):
            h = getattr(self, h)
        else:
            h = self._visitNode
        return h(node)


    def _visitNode(self, node):
        return self._visitChildren(node)


    def _visitChildren(self, node):
        for child in node.getChildNodes():
            self.visitNode(child)
        return



# this is just to demo overriding NodeVisitor
class Printer(NodeVisitor):
    
    def _visitNode(self, node):
        print node
        self._visitChildren(node)
        return


    def onAnd(self, node):
        print node
        print 'dict:', node.__dict__

        print node.left , node.right



# base of visitors that can transform node 
class Transformer(NodeVisitor):
    
    def visitNode(self, node):
        h = 'on%s' % node.__class__.__name__
        if hasattr(self, h):
            h = getattr(self, h)
        else:
            h = self._visitNode
        return h(node)


    def _visitNode(self, node):
        return self._visitChildren(node)


    def _visitChildren(self, node):
        for k, v in node.__dict__.iteritems():
            # skip private members
            if k.startswith('_'): continue
            
            if isinstance(v, list):
                nodes = v
                for index, child in enumerate(nodes):
                    if isinstance(child, tuple):
                        newchild = self._onTuple(child)
                    else:
                        newchild = self.visitNode(child)
                    
                    if newchild is not child:
                        nodes[index] = newchild
                    continue
            elif isinstance(v, ast.Node):
                child = v
                newchild = self.visitNode(child)
                if child is not newchild:
                    setattr(node, k, newchild)
        return node


    def _onTuple(self, t):
        new = []
        for item in t:
            if isinstance(item, ast.Node):
                newitem = self.visitNode(item)
                if newitem:
                    item = newitem
            new.append(item)
        return tuple(new)



# convert __and__ to __l_and__
class ConvertAndToLogicalAndCall(Transformer):


    def onAnd(self, node):
        f = ast.Name('logical_and')
        vs = node.nodes
        vs = [self.visitNode(n) for n in vs]
        return ast.CallFunc(f, vs)


    def onOr(self, node):
        f = ast.Name('logical_or')
        vs = node.nodes
        vs = [self.visitNode(n) for n in vs]
        return ast.CallFunc(f, vs)


converter = ConvertAndToLogicalAndCall()


# python 2.5 does not have a compiler to compiler ast.
# we only need a small compiler that works for our simple
# expression
class Compiler(NodeVisitor):

    def compile(self, ast, env):
        self.env = env
        return self.visitNode(ast)


    def visitNode(self, node):
        if isinstance(node, ast.Node):
            return super(Compiler, self).visitNode(node)
        return node


    def onConst(self, node):
        return node.value


    def onCompare(self, node):
        expr = node.expr
        lhs = self.visitNode(expr)
        
        ops = node.ops
        assert len(ops) == 1, 'Not implemented'
        op, rhs = ops[0]
        
        rhs = self.visitNode(rhs)
        
        return eval('lhs%srhs' % op, locals())


    def onName(self, node):
        name = node.name
        return eval(name, self.env)


    def onCallFunc(self, node):
        callee = self.visitNode(node.node)
        args = map(self.visitNode, node.args)

        star_args = node.star_args
        if star_args:
            star_args = map(self.visitNode, star_args)
            args = tuple(args) + tuple(star_args)

        dstar_args = node.dstar_args
        kwds = {}
        if dstar_args:
            for k, v in dstar_args.iteritems():
                kwds[k] = self.visitNode(v)
                
        return callee(*args, **kwds)


    def onExpression(self, node):
        return self.visitNode(node.node)



def parse(expr, context):
    'parse a filter expression and create syntax tree of the expression'

    # create the evaluation context
    from _logical_calls import calls
    env = calls.copy()
    env.update(context)

    # compile to ast
    a = compiler.parse(expr, mode='eval')
    # print ast.dump(a)
    
    # convert ast
    a1 = converter.visitNode(a)

    # compile ast
    compiler2 = Compiler()
    return compiler2.compile(a1, env)



def test1():
    root = compiler.parse('a==3 and b==4', mode='eval')
    # print root
    t = ConvertAndToLogicalAndCall().visitNode(root)
    # print root
    
    assert  not parse('a==3', {'a':1})
    assert  parse('a==3', {'a':3})
    return


def test2():
    from expression import measure
    a = measure('a')
    b = measure('b')
    env = {'a':a, 'b': b}
    print parse("a==3 and b==4", env)
    return


def test3():
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
    test1()
    test2()
    test3()
    return


if __name__=='__main__': main()


# version
__id__ = "$Id$"

# End of file 
