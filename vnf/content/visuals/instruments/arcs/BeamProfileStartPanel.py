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

    def build(self):
        director = self.director

        # container
        container = luban.content.document()

        # where am I?
        whereami = self.buildViewIndicator()
        container.add(whereami)

        # the main visual
        visual = luban.content.document(
            id='arcs-beam-profile-panel', title="Beam profile")
        visual.Class = 'app-container'
        container.add(visual)

        # toolbar
        toolbar = luban.content.toolbar(
            id='arcs-beam-toolbar', Class='app-toolbar')
        visual.add(toolbar)

        # reload button in toolbar
        reload = luban.content.load(
            actor='instruments/arcs', routine='loadApp', app='beam-profile')
        button = luban.content.button(
            label='Calculate a profile', onclick=reload)
        toolbar.add(button)
        # button to load profiles table
        loadprofilestable = luban.content.load(
            actor='instruments/arcs/beam-profile',
            routine='showProfilesTable')
        b = luban.content.button(label='Existing profiles', onclick=loadprofilestable)
        toolbar.add(b)

        doc = luban.content.document(id='arcs-beam-work-panel'); visual.add(doc)
        grid = luban.content.grid(id='arcs-beam-compute-profile-panel'); doc.add(grid)
        # grid.addClass('align-top')
        row = grid.row()
        # cell for user input
        inputcell = row.cell(Class='align-top')
        # cell for id holder
        idholdercell = row.cell()
        # cell for update button
        updatecell = row.cell(Class='align-top update-button-cell')
        # cell for plots
        plotscell = row.cell(Class='align-top')
        plotscell.addClass('app-output-cell')

        # input form
        inputcell.oncreate = luban.content.select(element=inputcell).append(
            luban.content.load(actor='orm/arcsbeamconfigurations', routine='edit')
            )

        #
        idholder = luban.content.paragraph(id='idholder', hidden=True)
        idholdercell.add(idholder)

        # update button
        update = luban.content.load(
            actor='instruments/arcs/beam-profile', 
            routine='update',
            id = luban.content.select(element=idholder).getAttr('text'),
            formids = luban.content.select(element=inputcell).findDescendentIDs(type='form'),
            )
        b = luban.content.button(label='===>>', onclick=update)
        b.tip = 'Run simulation or get simulation results'
        b.Class = 'run-button'
        updatecell.add(b)

        # output region
        doc = luban.content.document(id='output', title='Outputs')
        plotscell.add(doc)
        # doc.paragraph(text='Plots go here')
        doc.document(id='main-display-area')

        return container


# version
__id__ = "$Id$"

# End of file 
