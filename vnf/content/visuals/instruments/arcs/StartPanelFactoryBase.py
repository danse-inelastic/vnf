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


"""
base class for visuals that has the following structure

<input>     <run button>      <output>


"""



import luban.content


from ...AbstractFactory import AbstractFactory as base
class Factory(base):

    title = None # title of the visual. eg: "Beam profile"
    
    def __init__(self, director=None, name=None, actor=None):
        super(Factory, self).__init__(director=director, name=name, actor=actor)
        
        workpanelid_template = '%s-work-panel'
        self.workpanelid = workpanelid_template % self.name
        self.workgridid = '%s-work-grid'% self.name
        self.toolbarid = '%s-toolbar' % self.name
        return


    def buildToolbar(self):
        raise NotImplementedError


    def buildInputCellContent(self):
        raise NotImplementedError


    def buildUpdateButtonOnClickAction(self, inputcell, idholder):
        return luban.content.load(
            actor=self.actor, 
            routine='update',
            id = luban.content.select(element=idholder).getAttr('text'),
            formids = luban.content.select(element=inputcell)\
                .findDescendentIDs(type='form'),
            )


    def build(self, **kwds):
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
        doc = luban.content.document(id=self.workpanelid)
        visual.add(doc)
        grid = luban.content.grid(id=self.workgridid)
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
        # inputcell.oncreate = self.buildInputCellOnCreateAction(inputcell)
        inputcell.add(self.buildInputCellContent())

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
