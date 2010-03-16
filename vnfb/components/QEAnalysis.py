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
from vnfb.qeutils.pwoutput import PWOutput
from vnfb.qeutils.qegrid import QEGrid

import luban.content as lc
from luban.content import select, load
from luban.content.HtmlDocument import HtmlDocument

from luban.components.AuthorizedActor import AuthorizedActor as base

# Requires simulation id, config id and config type: (id, configid, type)
class Actor(base):

    class Inventory(base.Inventory):
        import pyre.inventory
        id          = pyre.inventory.str('id', default='')          # Simulation Id


    def default(self, director):
        return select(id='main-display-area').replaceContent(self.content(director))


    def content(self, director):
        doc         = lc.document(title="Analysis of Simulation Results")
        splitter    = doc.splitter(orientation="vertical")
        sInd        = splitter.section()                        # path indicator
        sAct        = splitter.section(id="qe-section-actions") # actions
        sSum        = splitter.section()                        # system summary
        sEle        = splitter.section()                        # system summary
        
        self._simrecord   = SimulationRecord(director, self.id)

        self._viewIndicator(director, sInd)
        self._showActions(director, sAct)  # Show actions
        self._summary(director, sSum)                     # System Summary
        self._electronStructure(director, sEle)           # Electron Structure
        self._simData()                     # Simulation Specific data

        return doc


    def _viewIndicator(self, director, section):
        path = []
        path.append(('Simulations ', load(actor='materialsimulation')))
        path.append(('Quantum Espresso ', load(actor='materialsimulation')))
        path.append(('%s ' % self.id, load(actor    = 'material_simulations/espresso/sim-view',
                                           id       = self.id)))

        path.append('Simulation Results')
        section.add(director.retrieveVisual('view-indicator', path=path))


    def _showActions(self, director, section):  #, inputs
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
                            onclick = load(actor      = 'material_simulations/espresso/analysis',
                                             id         = self.id))
                    )


    def _exportAction(self, container):
        "Export actions. Needs to be overwritten by subclasses"
        

    def _summary(self, director, section):
        "System Summary"


    def _electronStructure(self, director, section):
        "Electron Structure"

        # output exists
        section.add(lc.paragraph(text="Electron System", Class="qe-section"))
        table       = QEGrid(lc.grid(Class = "qe-table"))
        section.add(table.grid())

        pwoutput    = PWOutput(director, self.id)
        
        table.addRow(('Total Energy:', pwoutput.totalEnergy(True)))
        table.addRow(('Fermi Energy:', pwoutput.fermiEnergy(True)))
        table.setColumnStyle(0, "qe-cell-param")


    def _simData(self):
        "Simulation specific data. Should be overwritten by subclass"


    def _configure(self):
        super(Actor, self)._configure()
        self.id             = self.inventory.id


    def _init(self):
        super(Actor, self)._init()
        return

    def __init__(self, name):
        super(Actor, self).__init__(name=name)


__date__ = "$Mar 14, 2010 10:28:08 AM$"


