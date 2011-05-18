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

    title = 'I(Q,E) resolution'
    

    def buildToolbar(self):
        toolbar = luban.content.toolbar(id=self.toolbarid, Class='app-toolbar')

        # reload button in toolbar
        reload = luban.content.load(
            actor='instruments/arcs', routine='loadApp', app='iqe-resolution')
        button = luban.content.button(
            label='New computation', onclick=reload)
        toolbar.add(button)
        # button to load profiles table
        loadtable = luban.content.load(
            actor=self.actor,
            routine='showTable')
        b = luban.content.button(
            label='Existing computations',
            onclick=loadtable)
        toolbar.add(b)
        return toolbar


    def buildInputCellContent(self):
        return self.director.redirect(
            actor='orm/arcsiqeresolutioncomputations', 
            routine='edit',
            include_credential=False,
            )


# version
__id__ = "$Id$"

# End of file 
