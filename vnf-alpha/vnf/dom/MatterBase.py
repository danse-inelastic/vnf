# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from AbstractOwnedObjectBase import AbstractOwnedObjectBase as base
class MatterBase(base):

    name = 'matterbase'

    import dsaw.db

    cartesian_lattice = dsaw.db.doubleArray(
        name = 'cartesian_lattice', default = [1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0])
    cartesian_lattice.meta['tip'] = 'array of cartesian lattice vectors in Angstroms'
    
    fractional_coordinates = dsaw.db.doubleArray(
        name = 'fractional_coordinates', default = [])
    fractional_coordinates.meta['tip'] = 'array positions as fractional values of unit cell'
    
    cartesian_coordinates = dsaw.db.doubleArray(
        name = 'cartesian_coordinates', default = [])
    cartesian_coordinates.meta['tip'] = 'array positions as cartesian values of unit cell'
    
    atom_symbols = dsaw.db.varcharArray(
        name = 'atom_symbols', length = 2, default = [] )
    atom_symbols.meta['tip'] = 'atom symbols for each position in the unit cell'

    chemical_formula = dsaw.db.varchar(name = 'chemical_formula', length = 1024)
    

# version
__id__ = "$Id$"

# End of file 
