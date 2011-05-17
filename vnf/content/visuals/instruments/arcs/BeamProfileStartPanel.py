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

    title = 'Beam profile'
    

    def buildToolbar(self):
        toolbar = luban.content.toolbar(id=self.toolbarid, Class='app-toolbar')

        # reload button in toolbar
        reload = luban.content.load(
            actor='instruments/arcs', routine='loadApp', app='beam-profile')
        button = luban.content.button(
            label='Calculate a profile', onclick=reload)
        toolbar.add(button)
        # button to load profiles table
        loadprofilestable = luban.content.load(
            actor=self.actor,
            routine='showTable')
        b = luban.content.button(
            label='Existing profiles',
            onclick=loadprofilestable)
        toolbar.add(b)
        return toolbar


    def buildInputCellOnCreateAction(self, inputcell):
        return luban.content.select(element=inputcell).append(
            luban.content.load(
                actor='orm/arcsbeamconfigurations', 
                routine='edit')
            )
        
    
# version
__id__ = "$Id$"

# End of file 
