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

# XXX: Need to create text area
from _ import AbstractScatteringKernel as base, TableBase

LAZ_DEFAULT = "Please insert content of .laz file (e.g. Al.laz)!"

class PowderDiffractionKernel(base):

    dfraction   = 1e-5    # Dd_over_d
    dwfactor    = 1.      # DebyeWaller_factor
    lazcontent  = LAZ_DEFAULT      # Content of .laz file

    def customizeLubanObjectDrawer(self, drawer):
        drawer.sequence = ['properties']
        drawer.mold.sequence = [
            'dfraction',
            'dwfactor',
            'lazcontent'
            ]
        return


        def _createfield_for_lazcontent(obj):
            # this is a method of mold.
            self = drawer.mold

            # imports
            import luban.content as lc
            from luban.content import load, select
            from luban.content.FormTextArea import FormTextArea

            # widget
            doc     = lc.document(Class='container', id='lazcontent-content-container')
            content = FormTextArea(name='lazcontent', label='Content of .laz file')
            doc.add(content)
            
            return doc

        drawer.mold._createfield_for_lazcontent = _createfield_for_lazcontent

        return



InvBase = base.Inventory
class Inventory(InvBase):

    dfraction   = InvBase.d.float(name = 'dfraction', default = 1e-5)
    dwfactor    = InvBase.d.float(name = 'dwfactor', default = 1.)
    lazcontent  = InvBase.d.str(name = 'lazcontent', max_length = 65536, default = LAZ_DEFAULT)

    dbtablename = 'powderdiffractionkernels'

    pass


PowderDiffractionKernel.Inventory = Inventory
del Inventory

from _ import o2t
PowderDiffractionKernelTable = o2t(PowderDiffractionKernel, {'subclassFrom': TableBase},)

__date__ = "$Mar 8, 2011 9:27:32 PM$"


