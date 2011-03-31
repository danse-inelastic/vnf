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


from MonitorBase import MonitorBase as base, MonitorTableBase as TableBase
class NeutronRecorder(base):

    abstract = False
    
    def customizeLubanObjectDrawer(self, drawer):
        drawer.mold.sequence = [
            'componentname', 'short_description',
            'referencename', 'position', 'orientation',
            ]
    pass


InvBase=base.Inventory
class Inventory(InvBase):

    dbtablename = 'neutronrecorders'



NeutronRecorder.Inventory = Inventory
del Inventory


from _ import o2t
NeutronRecorderTable = o2t(NeutronRecorder, {'subclassFrom':TableBase})


# version
__id__ = "$Id$"

# End of file 
