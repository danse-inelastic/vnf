# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import numpy as N
def lattice(array):
    a = N.array(array)
    a.shape = 3, 3
    return a
    
def reciprocal(realspacelattice):
    l = lattice(realspacelattice)
    v = volume(l)
    pi = N.pi
    scale = 2*pi/v
    a1, a2, a3 = l
    b1 = N.cross(a2,a3)*scale
    b2 = N.cross(a3,a1)*scale
    b3 = N.cross(a1,a2)*scale
    return b1, b2, b3

def volume(vectors):
    v0, v1, v2 = vectors
    return N.dot(v0, N.cross(v1, v2))


# version
__id__ = "$Id$"

# End of file 
