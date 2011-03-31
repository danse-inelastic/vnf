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


    dateformat = 'YYYY-MM-DD'


    def render(self, expr):
        return expr.identify(self)


    def onEqual(self, expr):
        return self._onCompareOperator(expr, '=')
    

    def onLike(self, expr):
        v = expr.value
        v = v.replace('*', '%')
        measure = expr.measure
        if measure.type in ['str', 'link']:
            e = measure.name
        elif measure.type == 'date':
            e = "to_char(%s, '%s')" % (measure.name, self.dateformat)
        else:
            raise NotImplementedError, 'type: %s' % measure.type
        return '%s like %r' % (e, v)


    def _onCompareOperator(self, expr, op):
        return '%s %s %r' % (expr.measure.name, op, expr.value)
    
    
    def onAnd(self, expr):
        return self._onBinaryLogicalOperator(expr, 'and')
    

    def onOr(self, expr):
        return self._onBinaryLogicalOperator(expr, 'or')


    def _onBinaryLogicalOperator(self, expr, op):
        left = expr.left
        right = expr.right
        return '(%s) %s (%s)' % (left.identify(self), op, right.identify(self))


def test():
    from parser import parse
    
    from expression import measure
    renderer = AST2DBSyntax()

    a = measure('a')
    b = measure('b')
    env = {'a':a, 'b': b}
    print renderer.render(parse("a==3 and b==4", env))

    c = measure('c')
    env['c'] = c
    print renderer.render(parse('a==3 and b==4 and c==5', env))
    print renderer.render(parse('a==3 and b==4 or c==5', env))
    print renderer.render(parse('a==3 and (b==4 or c==5)', env))

    # like
    print renderer.render(parse('a=="*3*" and (b==4 or c==5)', env))

    # date type
    d = measure('d', type='date')
    env['d'] = d
    print renderer.render(parse('a=="*3*" and d=="*2010*"', env))
    return


def main():
    test()
    return

if __name__=='__main__': main()


# version
__id__ = "$Id$"

# End of file 
