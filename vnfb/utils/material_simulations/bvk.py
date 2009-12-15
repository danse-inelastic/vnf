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


# helpers for bvk. probably should move some of them to the bvk package
#  
#  * depends on sympy, numpy
#


import numpy

import sympy.matrices as matrices
import sympy
def _matrixelementsymbol(i,j):
    r = sympy.Symbol('m%s%s' % (i,j))
    return r
T = [ [_matrixelementsymbol(i,j) for j in range(3)] for i in range(3)]
T = matrices.Matrix(T)


def symmetryRestricted3X3Tensor(R):
    """find the restrictions to a 3X3 tensor given the transformation matrix
    of the symmetry operation.
    """
    R = matrices.Matrix(R)
    # R-1 * T * R = T
    equation = R.T * T * R - T
    from sympy.solvers import solve
    import operator
    equation = reduce(operator.add, equation.tolist())
    symbols = reduce(operator.add, T.tolist())
    solution = solve(equation, *symbols)
    return solution


def symmetriesRestricted3X3Tensor(Rs):
    """find the restrictions to a 3X3 tensor given the transformation matrices
    of the symmetry operations.
    """
    equations = _equationsForSymmetriesRestricted3X3Tensor(Rs)

    import operator
    symbols = reduce(operator.add, T.tolist())

    from sympy.solvers import solve
    solution = solve(equations, *symbols)
    
    return solution


def _equationsForSymmetriesRestricted3X3Tensor(Rs):
    Rs = map(matrices.Matrix, Rs)
    # R-1 * T * R = T
    equations = [R.T * T * R - T for R in Rs]
    import operator
    equations = [reduce(operator.add, equation.tolist())
                 for equation in equations]
    return reduce(operator.add, equations)
    

# depends on "matter" package
def findForceContantTensorRestrictions(vector, lattice, sg):
    """find the restrictions on force constant tensor (3X3) given
    the vector of the bond (in relative lattice coordinates), and
    the symmetry group.

    sg is an instance of matter.SpaceGroups.SpaceGroup. required methods are 'iter_symops_leave_vector_unchanged', which should return symmetry operations that has an attribute 'R' being 3X3 rotation matrix represented in relative lattice coordinates.
    lattice is an instance of matter.Lattice.Lattice. required attribute: 'stdbase', which is the matrix of base vectors in cartesian coordinates in standard orientation.
    vector is a vector of 3 in relative lattice coords
    """
    b = lattice.stdbase
    import numpy.linalg as nl
    binv = nl.inv(b)

    # the equations result from symmetry requirement of the bond
    def _R(symop):
        return numpy.dot(numpy.dot(binv, symop.R), b)
    Rs = [_R(symop) for symop in sg.iter_symops_leave_vector_unchanged(vector)]
    equations = _equationsForSymmetriesRestricted3X3Tensor(Rs)

    # add the equations for instrisic symmetry of force constant tensor
    equations += _intrinsicSymmetryEquationsForForceConstantTensor

    # the symbols to solve (9 matrix elements)
    import operator
    symbols = reduce(operator.add, T.tolist())

    # solve the equations
    from sympy.solvers import solve
    restrictions = solve(equations, *symbols)
    
    # need to convert restrictions dictionary to descriptor like
    _ = SympyExpression2ConstraintExpression()
    constraints = []
    for symbol, expression in restrictions.iteritems():
        # print 'sympy:', symbol, '=', expression
        var = _.render(symbol)
        expression = _.render(expression)
        constraints.append( var == expression )
    return constraints


# intrinsic symmetry of force constant tensor
_intrinsicSymmetryEquationsForForceConstantTensor = [
    T[0,1]-T[1,0],
    T[0,2]-T[2,0],
    T[1,2]-T[2,1],
    ]


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

    def test1(self):
        R = [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, -1],
            ]
        restrictions = symmetryRestricted3X3Tensor(R)
        assert restrictions[T[0,0]] == T[1,1]
        assert restrictions[T[0,1]] == T[1,0]
        assert restrictions[T[2,0]] == -T[2,1]
        assert restrictions[T[0,2]] == -T[1,2]
        return


    def test2(self):
        R = [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, -1],
            ]
        restrictions = symmetriesRestricted3X3Tensor([R])
        assert restrictions[T[0,0]] == T[1,1]
        assert restrictions[T[0,1]] == T[1,0]
        assert restrictions[T[2,0]] == -T[2,1]
        assert restrictions[T[0,2]] == -T[1,2]
        return


    def test3(self):
        R1 = [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, -1],
            ]
        R2 = [
            [1, 0, 0],
            [0, 0, 1],
            [0, -1, 0],
            ]
        restrictions = symmetriesRestricted3X3Tensor([R1, R2])
        self.assertEqual(restrictions[T[0,0]], T[2,2])
        self.assertEqual(restrictions[T[1,1]], T[2,2])
        self.assertEqual(restrictions[T[0,1]], 0)
        self.assertEqual(restrictions[T[0,2]], 0)
        self.assertEqual(restrictions[T[1,0]], 0)
        self.assertEqual(restrictions[T[1,2]], 0)
        self.assertEqual(restrictions[T[2,0]], 0)
        self.assertEqual(restrictions[T[2,1]], 0)
        return


    def test4(self):
        # fcc
        import matter
        lattice = matter.Lattice(a=1, b=1, c=1, alpha=90, beta=90, gamma=90)

        #
        from matter.SpaceGroups import sg225
        
        # 110
        vector = [0.5, 0.5, 0]
        print 'bond 110 for fcc lattice'
        for constraint in  findForceContantTensorRestrictions(vector, lattice, sg225):
            print constraint
            
        # 200
        vector = [1,0,0]
        print 'bond 200 for fcc lattice'
        for constraint in  findForceContantTensorRestrictions(vector, lattice, sg225):
            print constraint

        # 211
        vector = [1,0.5,0.5]
        print 'bond 211 for fcc lattice'
        for constraint in  findForceContantTensorRestrictions(vector, lattice, sg225):
            print constraint
            
        # 220
        vector = [1,1,0]
        print 'bond 220 for fcc lattice'
        for constraint in  findForceContantTensorRestrictions(vector, lattice, sg225):
            print constraint
            
        # 310
        vector = [1.5,0.5,0]
        print 'bond 310 for fcc lattice'
        for constraint in  findForceContantTensorRestrictions(vector, lattice, sg225):
            print constraint
            
        return


def main():
    unittest.main()
    return

if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
