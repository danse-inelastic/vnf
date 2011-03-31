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

"""
QEConvergence - base actor class for Quantum Espresso convergence pages
"""

ID_CONVERGENCE  = "qe-container-convergence"

from vnf.qeutils.qeutils import qeinput, defaultInputName, readRecordFile

import luban.content as lc
from luban.content import select, load

from luban.components.AuthorizedActor import AuthorizedActor as base

class QEConvergence(base):

    class Inventory(base.Inventory):
        import pyre.inventory
        id          = pyre.inventory.str('id', default='')          # Simulation Id


    def default(self, director):
        # Redirection doesn't pass value to self.id, so I need to do it manually

        return select(id='main-display-area').replaceContent(self.content(director))


    def content(self, director):
        "Contains of two separate splitters: header and results"
        self._setup(director)

        doc         = lc.document(title="Convergence Tests")
        splitter    = doc.splitter(orientation="vertical")
        sInd        = splitter.section()                        # path indicator
        sAct        = splitter.section(id="qe-section-actions") # actions

        docResults  = lc.document(id = ID_CONVERGENCE)
        doc.add(docResults)

        self._viewIndicator(director, sInd)
        self._showActions(director, sAct)                 # Show actions

        # Main content
        resSplitter = docResults.splitter(orientation="vertical")
        self._mainContent(director, resSplitter)              # Simulation Specific data

        return doc


    def _setup(self, director):
        "Init actor attributes"
        self._input = qeinput(director, self.id, linkorder=0)


    def _viewIndicator(self, director, section):
        qelink  = load( actor           = 'materialsimulation',
                        filter_key      = 'type',
                        filter_value    = 'qesimulations')

        path = []
        path.append(('Simulations ', load(actor='materialsimulation')))
        path.append(('Quantum Espresso ', qelink))
        path.append(('%s ' % self.id, load(actor    = 'material_simulations/espresso/sim-view',
                                           id       = self.id)))
        path.append('Convergence Tests')
        section.add(director.retrieveVisual('view-indicator', path=path))


    def _showActions(self, director, section):
#        self._backAction(section)
        self._refreshAction(section)
        self._newTestAction(section)
        self._pwInputAction(section)

        section.add(lc.document(Class="clear-both"))


#    def _backAction(self, section):
#        section.add(lc.link(label="Simulation",
#                            Class="qe-action-back",
#                            onclick = load(actor      = 'material_simulations/espresso/sim-view',
#                                             id         = self.id))
#                    )

    def _refreshAction(self, section):
        section.add(lc.link(label="Refresh",
                            Class="qe-action-back",
                            onclick = load(actor      = 'material_simulations/espresso-convergence/view',
                                             id       = self.id))
                    )

    def _newTestAction(self, section):
        section.add(lc.link(label="Create New Test",
                            Class="qe-action-new",
                            onclick = load(actor      = 'material_simulations/espresso-convergence/conv-create',
                                             id         = self.id))
                    )

    def _pwInputAction(self, section):
        "Shows PW input action button"
        if not self._input: # No input created
            section.add(lc.link(label="Create PW Input",
                                Class="qe-action-new",  
                                onclick = load(actor      = 'material_simulations/espresso/sim-view',
                                                 id         = self.id))
                        )
            return

        # Otherwise show PW link
        section.add(lc.link(label="PW",
                            Class="qe-action-default",  
                            onclick = load(actor    = 'material_simulations/espresso-convergence/input-view',
                                           inputid  = self._input.id,
                                           id       = self.id))
                    )

    # Taken from actors/material_simulations/espresso/input-edit.odb
    def _inputText(self, director, input):
        fname   = defaultInputName(input.type)
        s       = readRecordFile(director.dds, input, fname)
        if s:
            return s

        return ""


    def _mainContent(self, director, splitter):
        "Main content. Should be overwritten by subclass"


    def _configure(self):
        super(QEConvergence, self)._configure()
        self.id             = self.inventory.id


    def _init(self):
        super(QEConvergence, self)._init()


    def __init__(self, name):
        super(QEConvergence, self).__init__(name=name)


__date__ = "$Apr 22, 2010 5:29:03 PM$"


