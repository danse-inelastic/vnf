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


from Monitor import Monitor as base
class DetectorSystem_fromXML(base):

    tofmin = 3000.
    tofmax = 6000.
    ntofbins = 300
    pass


InvBase=base.Inventory
class Inventory(InvBase):

    tofmin = InvBase.d.float(name='tofmin', default=3000., validator=InvBase.v.positive)
    tofmin.tip = 'minimum tof. unit: microsecond'
    
    tofmax = InvBase.d.float( name = 'tofmax', default = 6000., validator=InvBase.v.positive)
    tofmax.tip = 'maximum tof. unit: microsecond'

    ntofbins = InvBase.d.int( name = 'ntofbins', default = 300 )
    ntofbins.tip = 'number of tof bins'

    dbtablename = 'detectorsystem_fromxmls'


DetectorSystem_fromXML.Inventory = Inventory
del Inventory


from _ import o2t, AbstractOwnedObjectBase
DetectorSystem_fromXMLTable = o2t(
    DetectorSystem_fromXML, {'subclassFrom': AbstractOwnedObjectBase})


# version
__id__ = "$Id$"

# End of file 
