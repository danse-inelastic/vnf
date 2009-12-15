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
#  * depends on sympy
#


import sympy.matrices as matrices
import sympy
T = [ ['t%s%s' % (i,j) for j in range(3)] for i in range(3)]
T = matrices.Matrix(T)


def symmetry_restricted_3X3_tensor(R):
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


import unittest
class TestCase(unittest.TestCase):

    def test1(self):
        R = [ [0, 1, 0],
              [1, 0, 0],
              [0, 0, -1],
              ]
        restrictions = symmetry_restricted_3X3_tensor(R)
        assert restrictions[T[0,0]] == T[1,1]
        assert restrictions[T[0,1]] == T[1,0]
        assert restrictions[T[2,0]] == -T[2,1]
        assert restrictions[T[0,2]] == -T[1,2]
        return


def main():
    unittest.main()
    return

if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
