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


from DbObject import DbObject
class MatterBase(DbObject):

    name = 'matterbase'

    import pyre.db

    cartesian_lattice = pyre.db.doubleArray(
        name = 'cartesian_lattice', default = [])
    cartesian_lattice.meta['tip'] = 'array of cartesian lattice vectors'
    
    fractional_coordinates = pyre.db.doubleArray(
        name = 'fractional_coordinates', default = [])
    fractional_coordinates.meta['tip'] = 'array positions as fractional values of unit cell'
    
    atom_symbols = pyre.db.varcharArray(
        name = 'atom_symbols', length = 2, default = [] )
    atom_symbols.meta['tip'] = 'atom symbols for each position in the unit cell'

    chemical_formula = pyre.db.varchar(
        name = 'chemical_formula', length = 1024)
    
    #shape_name = pyre.db.varchar( name = 'shape_name', length = 128 )
    #shape_name.meta['tip'] = 'the name of the shape: block, cylinder, etc.'
    
    #shape_parameters = pyre.db.varcharArray(
    #    name = 'shape_parameters', length = 128, default = [] )
    #shape_parameters.meta['tip'] = 'parameters of various sample shapes'




# version
__id__ = "$Id$"

# End of file 
