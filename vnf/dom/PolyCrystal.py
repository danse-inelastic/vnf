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
class PolyCrystal(base):

    name = 'polycrystals'

    import pyre.db



def inittable(db):
    def polycrystal( id, cartesian_lattice, fractional_coordinates,
                     atom_symbols, chemical_formula, short_description ):
        p = PolyCrystal()
        p.id = id
        p.cartesian_lattice = cartesian_lattice
        p.fractional_coordinates = fractional_coordinates
        p.atom_symbols = atom_symbols
        p.chemical_formula = chemical_formula
        p.short_description = short_description
        return p

    records = [
        polycrystal( 'polyxtalfccNi0',
                     [1.76,1.76,0,1.76,0,1.76,0,1.76,1.76],
                     [0,0,0],
                     ['Ni'],
                     'Ni',
                     'fcc Ni powder',
                     ),
        ]
    for r in records: db.insertRow( r )
    return


# version
__id__ = "$Id$"

# End of file 
