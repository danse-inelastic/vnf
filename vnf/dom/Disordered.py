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
    def disordered( id, creator, date, cartesian_lattice, fractional_coordinates,
                    atom_symbols, chemical_formula, short_description ):
        p = Disordered()
        p.id = id
        p.creator = creator
        p.date = date
        p.cartesian_lattice = cartesian_lattice
        p.fractional_coordinates = fractional_coordinates
        p.atom_symbols = atom_symbols
        p.chemical_formula = chemical_formula
        p.short_description = short_description
        return p

    records = [
        disordered( 'liquid0',
                    'vnf',
                    '2008/12/1',
                     [],
                     [],
                     [],
                     '?',
                    'some liquid sample good for sans experiment...',
                     ), 
        ]
    for r in records: db.insertRow( r )
    return


def initids():
    return [
        'liquid0',
        ]


# version
__id__ = "$Id$"

# End of file 
