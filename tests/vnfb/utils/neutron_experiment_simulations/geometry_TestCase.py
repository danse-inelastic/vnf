#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from vnfb.utils.neutron_experiment_simulations import geometry

I = [
    [1,0,0],
    [0,1,0],
    [0,0,1],
    ]
X90 = geometry.tomatrix((90,0,0))
Y90 = geometry.tomatrix((0,90,0))


from numpy.testing import assert_array_almost_equal


import unittest
class TestCase(unittest.TestCase):

    def test1(self):
        'calculateAbsoluteCoordinates'
        # simple: just one object "a"
        relative_coordinates = {
            'a': (None, (0,0,0), I)
            }
        abs = geometry.calculateAbsoluteCoordinates(relative_coordinates)
        pos, ori = abs['a']
        assert_array_almost_equal(pos, (0,0,0))
        assert_array_almost_equal(ori, I)

        # simple: b is relative to a
        relative_coordinates = {
            'a': (None, (0,0,0), I),
            'b': ('a', (1,2,3), I),
            }
        abs = geometry.calculateAbsoluteCoordinates(relative_coordinates)
        pos, ori = abs['a']
        assert_array_almost_equal(pos, (0,0,0))
        assert_array_almost_equal(ori, I)
        pos, ori = abs['b']
        assert_array_almost_equal(pos, (1,2,3))
        assert_array_almost_equal(ori, I)

        # simple: just switch a and b in the previous case
        relative_coordinates = {
            'b': (None, (0,0,0), I),
            'a': ('b', (1,2,3), I),
            }
        abs = geometry.calculateAbsoluteCoordinates(relative_coordinates)
        pos, ori = abs['b']
        assert_array_almost_equal(pos, (0,0,0))
        assert_array_almost_equal(ori, I)
        pos, ori = abs['a']
        assert_array_almost_equal(pos, (1,2,3))
        assert_array_almost_equal(ori, I)

        # simple, b rotated relative to a
        relative_coordinates = {
            'a': (None, (0,0,0), I),
            'b': ('a', (0,0,0), (90,0,0)),
            }
        abs = geometry.calculateAbsoluteCoordinates(relative_coordinates)
        pos, ori = abs['a']
        assert_array_almost_equal(pos, (0,0,0))
        assert_array_almost_equal(ori, I)
        pos, ori = abs['b']
        assert_array_almost_equal(pos, (0,0,0))
        assert_array_almost_equal(ori, X90)

        # a,b,c. b roated relative to a, c moved relative b
        relative_coordinates = {
            'a': (None, (0,0,0), I),
            'b': ('a', (0,0,0), (90,0,0)),
            'c': ('b', (0,1,0), I),
            }
        abs = geometry.calculateAbsoluteCoordinates(relative_coordinates)
        pos, ori = abs['a']
        assert_array_almost_equal(pos, (0,0,0))
        assert_array_almost_equal(ori, I)
        pos, ori = abs['b']
        assert_array_almost_equal(pos, (0,0,0))
        assert_array_almost_equal(ori, X90)
        pos, ori = abs['c']
        assert_array_almost_equal(pos, (0,0,1))
        assert_array_almost_equal(ori, X90)
        
        # a,b,c,d. b roated relative to a, c rotated relative b, d moved reltaive to c
        relative_coordinates = {
            'a': (None, (0,0,0), I),
            'b': ('a', (0,0,0), X90),
            'c': ('b', (0,0,0), Y90),
            'd': ('c', (0,0,1), I),
            }
        abs = geometry.calculateAbsoluteCoordinates(relative_coordinates)
        pos, ori = abs['a']
        assert_array_almost_equal(pos, (0,0,0))
        assert_array_almost_equal(ori, I)
        pos, ori = abs['b']
        assert_array_almost_equal(pos, (0,0,0))
        assert_array_almost_equal(ori, X90)
        pos, ori = abs['c']
        assert_array_almost_equal(pos, (0,0,0))
        assert_array_almost_equal(ori, geometry.tomatrix((90,90,0)))
        pos, ori = abs['d']
        assert_array_almost_equal(pos, (1,0,0))
        assert_array_almost_equal(ori, geometry.tomatrix((90,90,0)))
        
        return

    

def main():
    unittest.main()
    return



if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
