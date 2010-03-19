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
from vnfb.qeutils.results.pwresult import PWResult
from vnfb.qeutils.results.resultpath import ResultPath
from vnfb.qeutils.qegrid import QEGrid

import luban.content as lc
from luban.content import select, load

from luban.components.AuthorizedActor import AuthorizedActor as base

ID_RESULTS      = "qe-splitter-results" # id for results container
ID_OUTPUTS      = "qe-splitter-outputs"
CLASS_DEFAULT   = "qe-action-default"  # Default class
CLASS_ACTIVE    = "qe-color-blue"
CLASS_ERROR     = "qe-color-red"


# Requires simulation id, config id and config type: (id, configid, type)
class Actor(base):

    class Inventory(base.Inventory):
        import pyre.inventory
        id          = pyre.inventory.str('id', default='')          # Simulation Id
        type        = pyre.inventory.str('type', default='')        # Task type


    def default(self, director):
        # Redirection doesn't pass value to self.id, so I need to do it manually
        self.id     = self.inventory.id
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
        
        #self._simrecord   = SimulationRecord(director, self.id)
        self._pwresult    = PWResult(director, self.id)

        self._viewIndicator(director, sInd)
        self._showActions(director, sAct)                 # Show actions
        self._summary(director, sSum)                     # System Summary
        self._electronStructure(director, sEle)           # Electron Structure
        self._simData(resSplitter)                        # Simulation Specific data

        return doc


    def outputs(self, director):
        return [select(id=ID_RESULTS).replaceContent(self.contentOutput(director)),
                select(id=ID_OUTPUTS).replaceContent(self._outputLinks(director))
                ]


    def contentOutput(self, director):
        doc     = lc.document()
        visual  = 'material_simulations/espresso-analysis/outputs'
        doc.add(director.retrieveVisual(visual, director, self.id, self.type))

        return  doc


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
        self._outputAction(director, container)
        self._exportAction(director, container)

        section.add(lc.document(Class="clear-both"))


    def _backAction(self, container):
        "Back button"
        sBac     = container.section(Class="qe-section-back")
        sBac.add(lc.link(label="Back",
                        Class="qe-action-back",
                        onclick = load(actor      = 'material_simulations/espresso/sim-view',
                                         id         = self.id))
                )
        sBac.add(lc.link(label="Refresh",
                        Class="qe-action-edit",
                        onclick = load(actor      = 'material_simulations/espresso-analysis/electron',
                                         id         = self.id))
                )


    # XXX: Finish
    def _outputAction(self, director, container):
        "Simulation output files"
        sA          = container.section(Class="qe-section-text-output")
        sA.add(lc.htmldocument(text="Outputs: "))
        sB          = container.section()

        docOutput   = lc.document(id=ID_OUTPUTS)    # Hook for output links
        docOutput.add(self._outputLinks(director))
        sB.add(docOutput)


    def _outputLinks(self, director):
        "Output links"
        doc         = lc.document()         # Container for links
        simrecord   = SimulationRecord(director, self.id)
        typelist    = simrecord.typeList()    # simulation tasks type list 

        classes     = self._typeClasses(director, self.type, typelist)
        for l in typelist:
            doc.add(lc.link(label=l,
                            Class=classes[l],
                            onclick = load(actor      = 'material_simulations/espresso-analysis/electron', # XXX
                                           routine    = "outputs",
                                           type       = l,
                                           id         = self.id))
                    )

        return doc


    def _typeClasses(self, director, type, typelist):
        "Returns dictionary with class names for the specified type"
        classes = {}
        crash   = self._crashCheck(director, typelist)

        #assume(len(crash.keys()) == len(typelist))  # Assumption

        # Set default values first
        for t in typelist:
            classes[t]  = CLASS_DEFAULT
            if crash[t]:
                classes[t]   = "%s %s" % (CLASS_ERROR, classes[t])

        if not type in typelist:    # type is not recognized
            return classes

        if not crash[type]:     # Mark as active if it is not crashed only
            classes[type]   = CLASS_ACTIVE + " " + classes[type]

        return classes


    def _crashCheck(self, director, typelist):
        "Returns dictionary of crash tasks specified by type"
        crash   = {}
        for t in typelist:
            crash[t] = False # default to False (no crashed files)

        for t in typelist:
            resultpath  = ResultPath(director, self.id, t)
            path        = resultpath.resultFiles("crash")
            if path:    # has CRASH file
                crash[t]  = True

        return crash


#    def _exportAction(self, container):
#        "Export actions. Needs to be overwritten by subclasses"

    # XXX: Keep for presentation only
    def _exportAction(self, director, container):
        "Button related to export"
        simrecord   = SimulationRecord(director, self.id)
        sim         = simrecord.record()
        sA          = container.section()

        #if not sim and sim.type    == "Multiple Phonon":   # Make sure that jobs exist with DOS or Dispersion
        self._showPhononDos(sA, sim)
        self._showPhononDispersion(sA, sim)


    # XXX: Keep for presentation only
    def _showPhononDos(self, section, sim):
        linkDos     = lc.link(label="Export Phonon DOS",
                            Class="qe-action-edit",
                            onclick = load(actor        = 'material_simulations/espresso/phonondos',
                                            routine     = 'create',
                                            simid       = self.inventory.id))
        linkDos.tip = "Export Phonon DOS to Atomic Structure"

        # Uncomment
#        if self._phononDosCreated(sim):     # Check if DOS created
#            linkDos.label   = "Phonon DOS"
#            linkDos.onclick = load(actor        = 'atomicstructure',
#                                    routine     = 'showOverview',
#                                    id          = sim.structureid)  # matter id

        section.add(linkDos)


    # XXX: Keep for presentation only
    def _showPhononDispersion(self, section, sim):
       linkDisp     = lc.link(label="Export Phonon Dispersion",
                            Class="qe-action-edit",
                            onclick = load(actor        = 'material_simulations/espresso/phonons',
                                            routine     = 'create',
                                            simid       = self.inventory.id))
       linkDisp.tip = "Export Phonon Dispersion to Atomic Structure"
       section.add(linkDisp)



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


