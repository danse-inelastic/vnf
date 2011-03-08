# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from MonitorBase import MonitorBase as base
class VulcanDetectorSystem(base):

    abstract = False

    def customizeLubanObjectDrawer(self, drawer):
        drawer.sequence = [
            'properties',
            #'hierarchy',
            ]
        drawer.mold.sequence = [
            'componentname', 'short_description',
            'referencename', 'position', 'orientation',
            ]

InvBase=base.Inventory
class Inventory(InvBase):

#    tofmin = InvBase.d.float(name='tofmin', default=3000., validator=InvBase.v.positive)
#    tofmin.tip = 'minimum tof. unit: microsecond'
    pass

VulcanDetectorSystem.Inventory = Inventory
del Inventory


from _ import MonitorTableBase
VulcanDetectorSystemTable = o2t(
    VulcanDetectorSystem, {'subclassFrom': MonitorTableBase})

__date__ = "$Mar 8, 2011 11:57:08 AM$"


