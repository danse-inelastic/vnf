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


from SingleStructureViewFactory import Factory as base
class Factory(base):

    def create(self):
        view = lc.document(id='atomicstructure-details-view')

        titlebar = lc.splitter(Class='atomicstructure-details-view-title-bar')
        view.add(titlebar)

        # view indicator
        view_indicator = self.createViewIndicator()
        titlebar.section().add(view_indicator)

        #
        obj = self.atomicstructure
        director = self.director
        drawer = director.painter.paintObj.drawers.getDrawer(obj.__class__)

        editable = self.domaccess.isEditable(self.id)
        doc = drawer(obj, readonly=True, editlink=editable)
        view.add(doc)
        
        return view


# version
__id__ = "$Id$"

# End of file 
