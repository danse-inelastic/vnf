#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from vnfb.qeutils.qerecords import SimulationRecord
from vnfb.qeutils.pwresult import PWResult
from vnfb.qeutils.qegrid import QEGrid

import luban.content as lc
from luban.content import select, load
from luban.content.HtmlDocument import HtmlDocument

from luban.components.AuthorizedActor import AuthorizedActor as base

ID_RESULTS  = "qe-splitter-results" # id for results container

# Requires simulation id, config id and config type: (id, configid, type)
class Actor(base):

    class Inventory(base.Inventory):
        import pyre.inventory
        id          = pyre.inventory.str('id', default='')          # Simulation Id
        type        = pyre.inventory.str('type', default='')        # Task type


    def default(self, director):
        return select(id='main-display-area').replaceContent(self.content(director))


    def content(self, director):
        "Contains of two separate splitters: header and results"
        doc         = lc.document(title="Analysis of Simulation Results")
        splitter    = doc.splitter(orientation="vertical")
        sInd        = splitter.section()                        # path indicator
        sAct        = splitter.section(id="qe-section-actions") # actions

        docResults  = lc.document(id = ID_RESULTS)
        doc.add(docResults)
        
        resSplitter = docResults.splitter(orientation="vertical")
        sSum        = resSplitter.section()                        # system summary
        sEle        = resSplitter.section()                        # electron structure
        
        self._simrecord   = SimulationRecord(director, self.id)
        self._pwresult    = PWResult(director, self.id)

        self._viewIndicator(director, sInd)
        self._showActions(director, sAct)                 # Show actions
        self._summary(director, sSum)                     # System Summary
        self._electronStructure(director, sEle)           # Electron Structure
        self._simData(resSplitter)                        # Simulation Specific data

        return doc


    def outputs(self, director):
        return select(id=ID_RESULTS).replaceContent(self.contentOutput(director))


    def contentOutput(self, director):
        doc = lc.document(title="Hi")#, id=ID_RESULTS)
        visual  = 'material_simulations/espresso-analysis/outputs'
        #doc.add(director.retrieveVisual(visual, director, self.id))
        doc.add(lc.paragraph(text="System Summary"))
        sp  = lc.splitter()
        sec = sp.section()
        sec.add("Hi")

        return  doc #"Hi" #


    def _viewIndicator(self, director, section):
        path = []
        path.append(('Simulations ', load(actor='materialsimulation')))
        path.append(('Quantum Espresso ', load(actor='materialsimulation')))
        path.append(('%s ' % self.id, load(actor    = 'material_simulations/espresso/sim-view',
                                           id       = self.id)))

        path.append('Simulation Results')
        section.add(director.retrieveVisual('view-indicator', path=path))


    def _showActions(self, director, section):
        # Action splitter
        container   = lc.splitter(orientation="horizontal", id="qe-splitter-analysis")
        section.add(container)
        self._backAction(container)
        self._outputAction(container)
        self._exportAction(container)

        section.add(lc.document(Class="clear-both"))


    def _backAction(self, container):
        "Back button"
        s     = container.section(Class="qe-section-back")
        s.add(lc.link(label="Back",
                        Class="qe-action-back",
                        onclick = load(actor      = 'material_simulations/espresso/sim-view',
                                         id         = self.id))
                )

    # XXX: Finish
    def _outputAction(self, container):
        "Simulation output files"
        #container   = lc.splitter(orientation="horizontal") #"vertical")#
        sA          = container.section(Class="qe-section-text-output")
        sA.add(HtmlDocument(text="Outputs: "))
        sB          = container.section()

        typelist    = self._simrecord.typeList()    # simulation tasks type list

        for l in typelist:
            sB.add(lc.link(label=l,
                            Class="qe-action-edit",
                            onclick = load(actor      = 'material_simulations/espresso-analysis/electron', # XXX
                                           routine    = "outputs",
                                           type       = l,
                                           id         = self.id))
                    )


    def _exportAction(self, container):
        "Export actions. Needs to be overwritten by subclasses"
        

    def _summary(self, director, section):
        "System Summary"
        section.add(lc.paragraph(text="System Summary", Class="qe-section"))
        table       = QEGrid(lc.grid(Class = "qe-table-analysis"))
        section.add(table.grid())

        table.addRow(("Material Type:",     self._pwresult.materialType()))
        table.addRow(("Lattice Type:",      self._pwresult.latticeType()))
        table.addRow(("Atomic Structure:",  self._pwresult.atomicStructure()))   # "# Atom Position (bohr) Mass (u)  Pseudo-Potentials"
        table.addRow(("Energy Cutoff:",     self._pwresult.energyCutoff()))
        table.addRow(("Density Cutoff:",    self._pwresult.densityCutoff()))
        if self._pwresult.materialType() == "Metal":    # Parameters specific for metals
            table.addRow(("Smearing Type:",     self._pwresult.smearingType()))    # For metals only
            table.addRow(("Smearing Degree:",   self._pwresult.smearingDegree()))  # For metals only
        table.addRow(("K points:",          self._pwresult.kPoints()))

        table.setColumnStyle(0, "qe-cell-param-analysis")


    def _electronStructure(self, director, section):
        "Electron Structure"

        # output exists
        section.add(lc.paragraph(text="Electron System", Class="qe-section"))
        table       = QEGrid(lc.grid(Class = "qe-table-analysis"))
        section.add(table.grid())

        table.addRow(('Total Energy:',          self._pwresult.totalEnergy(True)))
        table.addRow(('Fermi Energy:',          self._pwresult.fermiEnergy(True)))
        table.addRow(("Forces:",                self._pwresult.forces()))
        table.addRow(("Stress (Ry/bohr^2):",    self._pwresult.stress()))

        table.setColumnStyle(0, "qe-cell-param-analysis")


    def _simData(self, splitter):
        "Simulation specific data. Should be overwritten by subclass"


    def _configure(self):
        super(Actor, self)._configure()
        self.id             = self.inventory.id
        self.type           = self.inventory.type


    def _init(self):
        super(Actor, self)._init()
        return

    def __init__(self, name):
        super(Actor, self).__init__(name=name)


__date__ = "$Mar 14, 2010 10:28:08 AM$"


