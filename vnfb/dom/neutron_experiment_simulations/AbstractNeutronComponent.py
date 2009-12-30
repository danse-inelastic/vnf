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

    short_description = ''
    
    pass # end of AbstractNeutronComponent


from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    short_description = InvBase.d.str(name='short_description')

AbstractNeutronComponent.Inventory = Inventory
del Inventory
    

# version
__id__ = "$Id$"

# End of file 
