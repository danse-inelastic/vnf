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
    actorname = 'instruments/arcs/iqe-resolution'
    ormactorname = 'orm/arcsiqeresolutioncomputations'

    def buildToolbar(self):
        toolbar = luban.content.toolbar(
            id='iqe-res-toolbar', Class='app-toolbar')

        # reload button in toolbar
        reload = luban.content.load(
            actor='instruments/arcs', routine='loadApp', app=self.name)
        button = luban.content.button(
            label='Calculate I(Q,E) resolution', 
            onclick=reload,
            )
        toolbar.add(button)
        # button to load resolution function table
        loadtable = luban.content.load(
            actor=self.actorname,
            routine='showTable')
        b = luban.content.button(
            label='Existing resolution functions',
            onclick=loadtable)
        toolbar.add(b)
        #
        return toolbar


    def buildInputCellOnCreateAction(self, inputcell):
        return luban.content.select(element=inputcell).append(
            luban.content.load(
                actor=self.ormactorname, 
                routine='edit')
            )
        
    
    def buildUpdateButtonOnClickAction(self, inputcell, idholder):
        return luban.content.load(
            actor=self.actorname, 
            routine='update',
            id = luban.content.select(element=idholder).getAttr('text'),
            formids = luban.content.select(element=inputcell)\
                .findDescendentIDs(type='form'),
            )


# version
__id__ = "$Id$"

# End of file 
