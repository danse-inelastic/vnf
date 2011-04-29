# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import numpy
import luban.content as lc


from SingleStructureEditorFactory import Factory as base
class Factory(base):

    def create(self):
        view = lc.document(id='edit-atomicstructure-details')

        titlebar = lc.splitter(Class='atomicstructure-details-view-title-bar')
        view.add(titlebar)

        # view indicator
        view_indicator = self.createViewIndicator()
        titlebar.section().add(view_indicator)

        #
        view.paragraph(text="This is not yet supported")
        
        return view


# version
__id__ = "$Id$"

# End of file 
