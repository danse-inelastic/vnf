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


class DetectorSystemHierarchy_fromXML:
    # detector system from xml. this is the core part of the detector system,
    # mostly unchangeable information of a detector system is here.
    # the tunable parameters are in DetectorSystem_fromXML
    pass


from _ import AbstractOwnedObjectBase as tbase, o2t
DetectorSystemHierarchy_fromXMLTable = o2t(
    DetectorSystemHierarchy_fromXML,
    {'subclassFrom': tbase},
    )
# a db record of DetectorSystemHierarchy_fromXML needs a xml file that contains
# the real specification of the detector system.
# it will be in the dedicated directory for the database record
DetectorSystemHierarchy_fromXMLTable.xmlfilename = 'detectorsystem.xml'
DetectorSystemHierarchy_fromXMLTable.datafiles = [DetectorSystemHierarchy_fromXMLTable.xmlfilename]


from MonitorBase import MonitorBase as base
class DetectorSystem_fromXML(base):

    abstract = False

    tofmin = 3000.
    tofmax = 6000.
    ntofbins = 300
    hierarchy = DetectorSystemHierarchy_fromXML()
    
    # the specification of the detector sytem itself is not yet defined here.
    # the detector system could be loaded from a xml file.
    
    def customizeLubanObjectDrawer(self, drawer):
        drawer.sequence = [
            'properties',
            'hierarchy',
            ]
        drawer.mold.sequence = [
            'componentname', 'short_description',
            'referencename', 'position', 'orientation',
            'tofmin', 'tofmax', 'ntofbins'
            ]
        
    pass


InvBase=base.Inventory
class Inventory(InvBase):
    
    tofmin = InvBase.d.float(name='tofmin', default=3000., validator=InvBase.v.positive)
    tofmin.tip = 'minimum tof. unit: microsecond'
    
    tofmax = InvBase.d.float( name = 'tofmax', default = 6000., validator=InvBase.v.positive)
    tofmax.tip = 'maximum tof. unit: microsecond'
    
    ntofbins = InvBase.d.int( name = 'ntofbins', default = 300, validator=InvBase.v.positive)
    ntofbins.tip = 'number of tof bins'

    hierarchy = InvBase.d.reference(name='hierarchy', targettype=DetectorSystemHierarchy_fromXML, owned=False)
    hierarchy.help = 'Detector system hierarchy'
    


DetectorSystem_fromXML.Inventory = Inventory
del Inventory


from _ import MonitorTableBase
DetectorSystem_fromXMLTable = o2t(
    DetectorSystem_fromXML, {'subclassFrom': MonitorTableBase})



# version
__id__ = "$Id$"

# End of file 
