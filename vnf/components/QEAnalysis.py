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

from vnf.qeutils.qeutils import analyseActor
from vnf.qeutils.qerecords import SimulationRecord
from vnf.qeutils.results.pwresult import PWResult
from vnf.qeutils.results.resultpath import ResultPath
from vnf.qeutils.qegrid import QEGrid

import luban.content as lc
from luban.content import select, load

ID_RESULTS      = "qe-splitter-results" # id for results container
ID_OUTPUTS      = "qe-splitter-outputs"
CLASS_DEFAULT   = "qe-action-default"  # Default class
CLASS_ACTIVE    = "qe-color-blue"
CLASS_ERROR     = "qe-color-red"

"""
QEAnalysis - base actor class for Quantum Espresso analysis pages
"""

from luban.components.AuthorizedActor import AuthorizedActor as base

class QEAnalysis(base):

    class Inventory(base.Inventory):
        import pyre.inventory
        id          = pyre.inventory.str('id', default='')          # Simulation Id
        simtype     = pyre.inventory.str('simtype', default='')
        type        = pyre.inventory.str('type', default='')        # Task type
        linkorder   = pyre.inventory.int('linkorder', default=-1)   


    def default(self, director):
        # Redirection doesn't pass value to self.id, so I need to do it manually
        self.id         = self.inventory.id
        self.linkorder  = self.inventory.linkorder
        return select(id='main-display-area').replaceContent(self.content(director))


    def content(self, director):
        "Contains of two separate splitters: header and results"
        doc         = lc.document(title="Analysis of Simulation Results")
        splitter    = doc.splitter(orientation="vertical")
        sInd        = splitter.section()                        # path indicator
        sAct        = splitter.section(id="qe-section-actions") # actions

        docResults  = lc.document(id = ID_RESULTS)
        doc.add(docResults)
        
        self._pwresult    = PWResult(director, self.id, linkorder = 0)  # From first "PW" task

        self._viewIndicator(director, sInd)
        self._showActions(director, sAct)                 # Show actions

        # Simulation Data
        resSplitter = docResults.splitter(orientation="vertical")
        self._simData(director, resSplitter)              # Simulation Specific data

        # System Summary and Electron Structure
        sSum        = resSplitter.section()                        # system summary
        sEle        = resSplitter.section()                        # electron structure
        self._summary(director, sSum)                     # System Summary
        self._electronStructure(director, sEle)           # Electron Structure

        return doc


    def outputs(self, director):
        "Displays the content of output files"
        return [select(id=ID_RESULTS).replaceContent(self._contentOutput(director)),
                select(id=ID_OUTPUTS).replaceContent(self._outputLinks(director))
                ]


    def export(self, director):
        "Displays exports page"
        return [select(id=ID_RESULTS).replaceContent(self._contentExport(director)),
                select(id=ID_OUTPUTS).replaceContent(self._outputLinks(director))
                ]


    def _contentOutput(self, director):
        doc     = lc.document()
        visual  = 'material_simulations/espresso-analysis/outputs'
        doc.add(director.retrieveVisual(visual, director, self.id, self.type, self.linkorder))

        return  doc


    def _contentExport(self, director):
        "Export content. "
        doc     = lc.document()
        doc.add("Nothing to export for %s" % self.simtype)

        return  doc


    def _viewIndicator(self, director, section):
        qelink  = load( actor           = 'materialsimulation',
                        filter_key      = 'type',
                        filter_value    = 'qesimulations')

        path = []
        path.append(('Simulations ', load(actor='materialsimulation')))
        path.append(('Quantum Espresso ', qelink))
        path.append(('%s ' % self.id, load(actor    = 'material_simulations/espresso/sim-view',
                                           id       = self.id)))

        path.append('Simulation Results')
        section.add(director.retrieveVisual('view-indicator', path=path))


    def _showActions(self, director, section):
        # Action splitter
        container   = lc.splitter(orientation="horizontal", id="qe-splitter-analysis")
        sMain        = container.section(Class="qe-section-back")    # Left actions
        section.add(container)
        self._backAction(sMain)
        self._refreshAction(sMain)
        self._exportAction(sMain)
        self._outputAction(director, container)

        section.add(lc.document(Class="clear-both"))


    def _backAction(self, section):
        "Back button"
        section.add(lc.link(label="Back",
                            Class="qe-action-back",
                            onclick = load(actor      = 'material_simulations/espresso/sim-view',
                                             id       = self.id))
                    )

    def _refreshAction(self, section):
        "Refresh button"
        section.add(lc.link(label="Refresh",
                            Class="qe-action-edit",
                            onclick = load(actor    = analyseActor(self.simtype),
                                           simtype  = self.simtype,     # pass simtype
                                           id       = self.id))
                    )



    def _exportAction(self, section):
        "Export button"
        link     = lc.link(label="Export",
                            Class="qe-action-edit",
                            onclick = load(actor    = analyseActor(self.simtype), #'material_simulations/espresso-analysis/exports',
                                            routine = "export",
                                            id      = self.id,
                                            simtype = self.simtype),
                           tip = "Export Parameters of the Simulation"                 
                           )
        section.add(link)


    def _outputAction(self, director, container):
        "Simulation output files"
        sA          = container.section(Class="qe-section-text-output")
        sA.add(lc.htmldocument(text="Outputs: "))
        sB          = container.section(Class="qe-section-output")

        docOutput   = lc.document(id=ID_OUTPUTS)    # Hook for output links
        docOutput.add(self._outputLinks(director))
        sB.add(docOutput)


    def _outputLinks(self, director):
        "Output links"
        doc         = lc.document()         # Container for links
        simrecord   = SimulationRecord(director, self.id)
        typelist    = simrecord.typeList()  # simulation tasks type list, populated from SIMCHAINS
        chainsize   = len(typelist)

        classes     = self._typeClasses(director, self.linkorder, chainsize)

        for i in range(chainsize):
            doc.add(lc.link(label   = typelist[i], 
                            Class   = classes[i],
                            onclick = load(actor      = analyseActor(self.simtype), # XXX
                                           routine    = "outputs",
                                           type       = typelist[i],
                                           simtype    = self.simtype,
                                           id         = self.id,
                                           linkorder  = i))
                    )

        return doc


    def _typeClasses(self, director, linkorder, chainsize):
        "Returns list with class names for the specified linkorder"
        classes = [CLASS_DEFAULT for i in range(chainsize)] # Set default values first
        crash   = self._crashCheck(director, chainsize)

        assert(len(crash) == chainsize)  # Assumption

        
        for i in range(len(classes)):
            if crash[i]:
                classes[i]   = "%s %s" % (CLASS_ERROR, classes[i])

        if not linkorder in range(chainsize):    # linkorder is out of range
            return classes

        if not crash[linkorder]:     # Mark as active if it is not crashed only
            classes[linkorder]   = CLASS_ACTIVE + " " + classes[linkorder]

        return classes


    def _crashCheck(self, director, chainsize):
        "Returns list of crash tasks specified"
        crash   = [False for i in range(chainsize)]    # default to False (no crashed files)

        for i in range(len(crash)):
            resultpath  = ResultPath(director, self.id, i)
            path        = resultpath.resultFiles("crash")
            if path:    # has CRASH file
                crash[i]  = True

        return crash


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


    def _simData(self, director, splitter):
        "Simulation specific data. Should be overwritten by subclass"


    def _configure(self):
        super(QEAnalysis, self)._configure()
        self.id             = self.inventory.id
        self.type           = self.inventory.type
        self.simtype        = self.inventory.simtype
        self.linkorder      = self.inventory.linkorder


    def _init(self):
        super(QEAnalysis, self)._init()


    def __init__(self, name):
        super(QEAnalysis, self).__init__(name=name)


__date__ = "$Mar 14, 2010 10:28:08 AM$"


