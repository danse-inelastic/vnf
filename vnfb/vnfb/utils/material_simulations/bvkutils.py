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


# depends on "bvk", "matter"

# depends on "matter" package
def findForceContantTensorConstraints(bond):
    """find the constraints of force constant tensor given the bvk bond, which
    is an instance of BvKBond
    """
    restrictions = bond.getConstraints()

    # need to convert restrictions dictionary to descriptor like
    _ = SympyExpression2ConstraintExpression()
    constraints = []
    for symbol, expression in restrictions:
        # print 'sympy:', symbol, '=', expression
        var = _.render(symbol)
        expression = _.render(expression)
        constraints.append( var == expression )
    return constraints


# visitor to sympy expression to construct vnfb.utils.constraints expression
from vnfb.utils import constraints
class SympyExpression2ConstraintExpression(object):


    def render(self, expression):
        if self.isNumber(expression): return expression
        return self.dispatch(expression)


    def isNumber(self, candidate):
        return isinstance(candidate, int) or \
               isinstance(candidate, float)


    def dispatch(self, expression):
        name = 'on'+expression.__class__.__name__.capitalize()
        method = getattr(self, name)
        return method(expression)


    def onAdd(self, expression):
        right, left = expression.as_two_terms()
        left = self.render(left)
        right = self.render(right)
        return left+right


    def onMul(self, expression):
        right, left = expression.as_two_terms()
        left = self.render(left)
        right = self.render(right)
        try:
            return left*right
        except:
            return right*left


    def onSymbol(self, symbol):
        var = VarFromSympySymbol(symbol)
        return var


    def onZero(self, symbol):
        return 0


    def onNegativeone(self, symbol):
        return -1
    

# special var to represent sympy symbol
class VarFromSympySymbol(constraints.Variable):

    def __init__(self, symbol):
        self.symbol = symbol
        self.name = symbol.name
        return


    def __str__(self):
        return self.name


        

import unittest
class TestCase(unittest.TestCase):

    def test4(self):
        # fcc
        import matter
        lattice = matter.Lattice(a=1, b=1, c=1, alpha=90, beta=90, gamma=90)

        #
        from matter.SpaceGroups import sg225
        
        # 110
        vector = [0.5, 0.5, 0]
        print 'bond 110 for fcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg225):
            print constraint
            
        # 200
        vector = [1,0,0]
        print 'bond 200 for fcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg225):
            print constraint

        # 211
        vector = [1,0.5,0.5]
        print 'bond 211 for fcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg225):
            print constraint
            
        # 220
        vector = [1,1,0]
        print 'bond 220 for fcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg225):
            print constraint
            
        # 310
        vector = [1.5,0.5,0]
        print 'bond 310 for fcc lattice'
        for constraint in  findForceContantTensorConstraints(vector, lattice, sg225):
            print constraint
            
        return


def main():
    unittest.main()
    return

if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
