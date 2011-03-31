# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


'''base class of sample components.

!!! please note that SampleComponent is not derived from SampleBase. SampleComponent is special, please read documentation there for details.
'''

from AbstractNeutronComponent import AbstractNeutronComponent as base


# data object base class
class SampleBase(base):

    pass 



# orm Inventory base class
class Inventory(base.Inventory):

    pass

SampleBase.Inventory = Inventory
del Inventory



# db table base class
from _ import NeutronComponentTableBase
class TableBase(NeutronComponentTableBase):

    import dsaw.db

    # whether the record is just a configuration or not
    isconfiguration = dsaw.db.boolean(name='isconfiguration', default=False)
    


# version
__id__ = "$Id$"

# End of file 
