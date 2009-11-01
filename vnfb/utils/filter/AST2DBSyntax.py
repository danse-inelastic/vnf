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


class AST2DBSyntax(object):


    def render(self, expr):
        return expr.identify(self)


    def onEqual(self, expr):
        return self._onCompareOperator(expr, '=')

    def onLike(self, expr):
        v = expr.value
        v = v.replace('*', '%')
        return '%s like %r' % (expr.measure, v)


    def _onCompareOperator(self, expr, op):
        return '%s %s %r' % (expr.measure, op, expr.value)


    def onAnd(self, expr):
        return self._onBinaryLogicalOperator(expr, 'and')
    
    def onOr(self, expr):
        return self._onBinaryLogicalOperator(expr, 'or')


    def _onBinaryLogicalOperator(self, expr, op):
        left = expr.left
        right = expr.right
        return '(%s) %s (%s)' % (left.identify(self), op, right.identify(self))


def test():
    from expression import measure
    length = measure('length')

    renderer = AST2DBSyntax()
    print renderer.render(length==3)

    radius = measure('radius')
    print renderer.render( (length==3) & (radius==4))
    return


def main():
    test()
    return

if __name__=='__main__': main()


# version
__id__ = "$Id$"

# End of file 
