# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2007-2010 All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class AbstractNeutronComponent(object):

    componentname = ''
    position = [0.,0.,0.]
    orientation = [[1.,0.,0.],
                   [0.,1.,0.],
                   [0.,0.,1.],]
    referencename = ''

    short_description = ''

    pass # end of AbstractNeutronComponent


from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    componentname = InvBase.d.str(name='componentname')
    position = InvBase.d.array(name='position', elementtype='float', shape=3)
    orientation = InvBase.d.array(name='orientation', elementtype='float', shape=(3,3))
    referencename = InvBase.d.str(name='referencename')

    short_description = InvBase.d.str(name='short_description')


AbstractNeutronComponent.Inventory = Inventory
del Inventory


# version
__id__ = "$Id$"

# End of file 
