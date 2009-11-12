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


from dsaw.db.GloballyReferrable import GloballyReferrable as base


class BvKBond(base):

    name = 'bvkbonds'

    import dsaw.db

    id = dsaw.db.varchar(name='id', length=64)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"
    
    A = dsaw.db.integer(name='A')
    B = dsaw.db.integer(name='B')

    Boffset = dsaw.db.doubleArray(name='Boffset', default=[0,0,0], shape=3)

    force_constant_matrix = dsaw.db.doubleArray(
        name='force_constant_matrix', default=[0,0,0,0,0,0,0,0,0,], shape=(3,3))
    
    bond_is_mutable = dsaw.db.boolean(name='bond_is_mutable', default=True)
    

# version
__id__ = "$Id$"

# End of file 
