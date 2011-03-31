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


# visitor to sympy expression to construct vnf.utils.constraints expression
from vnf.utils import constraints
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


    def onReal(self, symbol):
        return float(symbol)
    

# special var to represent sympy symbol
class VarFromSympySymbol(constraints.Variable):

    def __init__(self, symbol):
        self.symbol = symbol
        self.name = symbol.name
        return


    def __str__(self):
        return self.name


        
# version
__id__ = "$Id$"

# End of file 
