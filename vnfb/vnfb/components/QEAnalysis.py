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

from vnfb.utils.qerecords import SimulationRecord

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
        sA          = splitter.section()                        # path indicator
        sB          = splitter.section(id="qe-section-actions") # actions

        simrecord   = SimulationRecord(director, self.id)
        #sim         = simrecord.record()
        self._viewIndicator(director, sA)
        self._showActions(sB, simrecord)               # Show actions

        # - System Summary
        # - Electron System

        return doc


#    def _document(self, director):
#        pass


    def _viewIndicator(self, director, section):
        path = []
        path.append(('Simulations ', load(actor='materialsimulation')))
        path.append(('Quantum Espresso ', load(actor='materialsimulation')))
        path.append(('%s ' % self.id, load(actor    = 'material_simulations/espresso/sim-view',
                                           id       = self.id)))

        path.append('Simulation Results')
        section.add(director.retrieveVisual('view-indicator', path=path))


    def _showActions(self, section, sim):  #, inputs
        # Action splitter
        container   = lc.splitter(orientation="horizontal", id="qe-splitter-analysis")
        section.add(container)
        self._backAction(container)
        self._outputAction(container, sim)
        self._exportAction(container, sim)

        section.add(lc.document(Class="clear-both"))


    def _backAction(self, container):
        "Back button"
        s     = container.section(Class="qe-section-back")
        s.add(lc.link(label="Back",
                        Class="qe-action-back",
                        onclick = load(actor      = 'material_simulations/espresso/sim-view',
                                         id         = self.id))
                )


    def _outputAction(self, container, simrecord):
        "Simulation output files"
        #container   = lc.splitter(orientation="horizontal") #"vertical")#
        sA          = container.section(Class="qe-section-text-output")
        sA.add(HtmlDocument(text="Outputs: "))
        sB          = container.section()

        typelist    = simrecord.typeList()

        for l in typelist:
            sB.add(lc.link(label=l,
                            Class="qe-action-edit",
                            onclick = load(actor      = 'material_simulations/espresso/analysis',
                                             id         = self.id))
                    )


    def _exportAction(self, container, sim):
        "Export actions. Needs to be overwritten by subclasses"
        

    def _configure(self):
        super(Actor, self)._configure()
        self.id             = self.inventory.id


    def _init(self):
        super(Actor, self)._init()
        return

    def __init__(self, name):
        super(Actor, self).__init__(name=name)


__date__ = "$Mar 14, 2010 10:28:08 AM$"


