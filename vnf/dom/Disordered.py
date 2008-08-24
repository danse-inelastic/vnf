# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from MatterBase import MatterBase as base
class Disordered(base):

    name = 'disordered'

    import pyre.db


def inittable(db):
    def disordered( id, cartesian_lattice, fractional_coordinates,
                    atom_symbols, chemical_formula ):
        p = Disordered()
        p.id = id
        p.cartesian_lattice = cartesian_lattice
        p.fractional_coordinates = fractional_coordinates
        p.atom_symbols = atom_symbols
        p.chemical_formula = chemical_formula
        return p

    records = [
        disordered( 'liquid0',
                     [],
                     [],
                     [],
                     '?',
                     ),
        ]
    for r in records: db.insertRow( r )
    return



# version
__id__ = "$Id$"

# End of file 
