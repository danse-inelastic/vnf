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


from _ import o2t


# data object
class PhononDOS:

    matter = None



# orm
from vnfb.dom.AtomicStructure import Structure

from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    matter = InvBase.d.reference(
        name='matter', targettype=None, targettypes=[Structure], owned=0)

    dbtablename = 'phonondoses'

PhononDOS.Inventory = Inventory


# db table
from ComputationResult import ComputationResult
PhononDOSTable = o2t(PhononDOS, {'subclassFrom': ComputationResult})
PhononDOSTable.datafiles = [
    'data.idf',
    ]


# view
def customizeLubanObjectDrawer(self, drawer):
    def createReadOnlyView(obj, editlink=None):
        # the document to build
        import luban.content as lc
        doc = lc.document(title='Phonon DOS')
        
        # the idf file
        path = drawer.obj_resource_path
        import os
        f = os.path.join(path, 'data.idf')
        
        # check path
        if not os.path.exists(f): return

        # read
        from idf import DOS
        (t,version,comment), e, i = DOS.read(f)

        # plot
        p = lc.plot2d(width=480, height=320)
        p.curve(x=list(e), y=list(i), label='Density of states')

        #
        doc.add(p)
        
        return doc
    drawer.createReadOnlyView = createReadOnlyView
    return
PhononDOS.customizeLubanObjectDrawer = customizeLubanObjectDrawer


# version
__id__ = "$Id$"

# End of file 
