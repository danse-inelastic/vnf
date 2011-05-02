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

class Factory(object):

    name = None # name of this factory. eg: "arcs-beam-profile"
    title = None # title of the visual. eg: "Beam profile"

    def __init__(self, director):
        self.director = director
        return


    def buildToolbar(self):
        raise NotImplementedError


    def buildInputCellOnCreateAction(self, inputcell):
        raise NotImplementedError


    def buildUpdateButtonOnClickAction(self, inputcell, idholder):
        raise NotImplementedError


    def build(self):
        director = self.director

        # container
        container = luban.content.document()

        # where am I?
        whereami = self.buildViewIndicator()
        container.add(whereami)

        # the main visual
        visual = luban.content.document(
            id='%s-panel' % self.name, title=self.title)
        visual.Class = 'app-container'
        container.add(visual)

        # toolbar
        toolbar = self.buildToolbar()
        visual.add(toolbar)

        # the input -> run button -> output structure
        doc = luban.content.document(id='%s-work-panel' % self.name); 
        visual.add(doc)
        grid = luban.content.grid(id='%s-compute-profile-panel'% self.name);
        doc.add(grid)
        # grid.addClass('align-top')
        row = grid.row()
        # cell for user input
        inputcell = row.cell(Class='align-top')
        # cell for id holder
        idholdercell = row.cell()
        # cell for update button
        updatecell = row.cell(Class='align-top update-button-cell')
        # cell for plots
        outputcell = row.cell(Class='align-top')
        outputcell.addClass('app-output-cell')

        # input form
        inputcell.oncreate = self.buildInputCellOnCreateAction(inputcell)

        #
        idholder = luban.content.paragraph(id='idholder', hidden=True)
        idholdercell.add(idholder)

        # update button
        update = self.buildUpdateButtonOnClickAction(inputcell, idholder)
        b = luban.content.button(label='===>>', onclick=update)
        b.tip = 'Run simulation or get simulation results'
        b.Class = 'run-button'
        updatecell.add(b)

        # output region
        doc = luban.content.document(id='output', title='Outputs')
        outputcell.add(doc)
        # doc.paragraph(text='Plots go here')
        doc.document(id='main-display-area')

        return container


    def buildViewIndicator(self):
        # where am I?
        path = [
            ('<< ARCS portal', 
             luban.content.load(
                    actor='instruments/arcs', 
                    routine='reloadStartPanel'
                    )
             ),
            ]
        from ... import view_indicator
        whereami = view_indicator.visual(path)
        return whereami


# version
__id__ = "$Id$"

# End of file 
