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


# activate customized orm in vnf for atomic structure
import vnf.dom.AtomicStructure


# deactivate the warning from importing bvk
import journal
journal.warning('UserWarning').deactivate()
import bvk
#
journal.warning('UserWarning').activate()



from bvk.orm.BvKModel import BvKModel


# view
def customizeLubanObjectDrawer(self, drawer):
    drawer.sequence = ['properties', 'bonds']
    drawer.readonly_view_sequence = ['matter', 'properties', 'bonds']
BvKModel.customizeLubanObjectDrawer = customizeLubanObjectDrawer

from _ import o2t
BvKModel_Table = o2t(BvKModel)


# version
__id__ = "$Id$"

# End of file 
