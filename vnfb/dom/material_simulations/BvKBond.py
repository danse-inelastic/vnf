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


from dsaw.model.Inventory import Inventory as InvBase

class BvKBond(object):


    class Inventory(InvBase):

        A = InvBase.d.int(name='A')
        B = InvBase.d.int(name='B')

        Boffset = InvBase.d.array(
            name='Boffset', elementtype='float',
            default=[0,0,0], shape=3)

        force_constant_matrix = InvBase.d.array(
            name='force_constant_matrix', elementtype='float',
            default=[0,0,0,0,0,0,0,0,0,], shape=(3,3))
    

        dbtablename = 'bvkbonds'


# version
__id__ = "$Id$"

# End of file 
