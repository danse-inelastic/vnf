# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import luban.content
from StartPanelFactoryBase import Factory as base

class Factory(base):

    name = 'arcs-iqe-resolution'
    title = 'I(Q,E) resolution'
    

    def build(self):
        director = self.director

        # container
        container = luban.content.document()

        # where am I?
        whereami = self.buildViewIndicator()
        container.add(whereami)

        appcontainer = container.document(id='tmp', Class='app-container')
        appcontainer.paragraph(text = "Coming soon...")
        return container


    def buildToolbar(self):
        toolbar = luban.content.toolbar(
            id='iqe-res-toolbar', Class='app-toolbar')
        return toolbar


    def buildInputCellOnCreateAction(self, inputcell):
        return luban.content.alert("not implemented yet")
        
    
    def buildUpdateButtonOnClickAction(self, inputcell, idholder):
        return luban.content.alert("not implemented yet")


# version
__id__ = "$Id$"

# End of file 
