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
class SingleCrystal(base):

    name = 'singlecrystals'

    import pyre.db


def inittable(db):
    def record( id, creator, date, cartesian_lattice, fractional_coordinates,
                atom_symbols, chemical_formula, short_description ):
        r = SingleCrystal()
        r.id = id
        r.creator = creator
        r.date = date
        r.cartesian_lattice = cartesian_lattice
        r.fractional_coordinates = fractional_coordinates
        r.atom_symbols = atom_symbols
        r.chemical_formula = chemical_formula
        r.short_description = short_description
        return r

    records = [
        record(
            'silicon_diamond',
            'vnf', '2008/12/1',
            [2.716,2.716,0, 2.716,0,2.716, 0,2.716,2.716],
            [0,0,0, 0.25,0.25,0.25],
            ['Si', 'Si'],
            'Si',
            'Si (diamond structure)',
            ),
        ]
    for r in records: db.insertRow( r )
    return


def initids():
    return [
        'silicon_diamond',
        ]


# version
__id__ = "$Id$"

# End of file 
