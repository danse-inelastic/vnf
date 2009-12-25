#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                     (C) 2007-2009  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def crystal2xyz( crystal ):
    # convert a crystal db record to a xyz file
    lattice = crystal.cartesian_lattice
    coords= crystal.fractional_coordinates
    atoms = crystal.atom_symbols
   
    from numpy import array
    coords = array(coords)
    coords.shape = -1,3
   
    assert len(atoms) == len(coords)

    contents = []
    contents.append( '%d' % len(atoms) )
    contents.append( ' '.join( [ '%s' % a for a in lattice ] ) )
    for atom, coord in zip( atoms, coords):
        contents.append(
            '%s %s' % (atom, ' '.join( [ '%s' % x for x in coord] ) )
            )
        continue
   
    return contents



# version
__id__ = "$Id$"

# End of file 
