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

import luban.content as lc
from luban.content import select, load
from vnfb.qeutils.qeparser.qeinput import QEInput
import vnfb.qeutils.filters as filters


from luban.components.AuthorizedActor import AuthorizedActor as base

"""
QEGenerator - base actor class for Quantum Espresso generator pages

Notes:
    - Inventory for parameters is used in methods (e.g. self.inventory.id) to properly
    pass parameters with director.redirect()
"""

class QEGenerator(base):

    class Inventory(base.Inventory):
        import pyre.inventory
        # Simulation attributes
        id          = pyre.inventory.str('id', default='')          # Simulation id
        simtype     = pyre.inventory.str('simtype', default='')     # Simulation type
        structureid = pyre.inventory.str('structureid', default='') # Atomic structure id
        # Task attributes
        taskid      = pyre.inventory.str('taskid', default='')      # Task id
        type        = pyre.inventory.str('type', default='')        # Task type
        subtype     = pyre.inventory.str('subtype', default='')
        # Input attributes
        fname       = pyre.inventory.str('fname', default='')
        description = pyre.inventory.str('description', default='')
        text        = pyre.inventory.str('text', default='')
        linkorder   = pyre.inventory.str('linkorder', default='')   # Linkorder, if not set from qeconst.py


    def default(self, director):
        "Default routine"
        return select(id='main-display-area').replaceContent(self.content(director))


    def content(self, director):
        "Populates the content for creation of input configuration"
        title   = "Create Input Configuration: %s" % self.type
        label   = "Select Option"
        return self._document(director, title, label)


    def _document(self, director, title, label, formMethod = "defaultForm", visual = None):
        doc         = lc.document(title = title)
        splitter    = doc.splitter(orientation = "vertical")
        sA          = splitter.section()
        sB          = splitter.section()
        sA.add(self._viewIndicator(director, label))
        sB.add(getattr(self, formMethod)(director, visual))

        return doc


    def _viewIndicator(self, director, label):
        "Displays the navigation path on the top"
        # director.redirect() does not pass variables. Get them from inventory instead
        self.id     = self.inventory.id
        self.taskid = self.inventory.taskid
        self.type   = self.inventory.type

        qelink  = load( actor           = 'materialsimulation',
                        filter_key      = 'type',
                        filter_value    = 'qesimulations')

        path = []
        path.append(('Simulations ',        load(actor='materialsimulation')))
        path.append(('Quantum Espresso ',   qelink))
        path.append(('%s ' % self.id,       load(actor    = 'material_simulations/espresso/sim-view',
                                                id       = self.id)))
        path.append(('%s Task ' % self.type, load(actor    = 'material_simulations/espresso/task-view',
                                                  id       = self.id,
                                                  taskid   = self.taskid,
                                                  type     = self.type)))
        path.append(label)
        return director.retrieveVisual('view-indicator', path=path)


    def defaultForm(self, director, visual):
        "Default implementation of input form"
        visual_     = "material_simulations/espresso/input-default"
        if visual:      # set visual if passed
            visual_ = visual

        return director.retrieveVisual(visual_,
                                       actor        = self.inventory,
                                       director     = director,
                                       simtype      = self.simtype,
                                       structureid  = self.structureid)


    def filterInput(self, director):
        "Default behaviour: standard filtering"
        input   = QEInput(config=self.inventory.text, type=self.inventory.type)
        filter  = filters.filterFactory(self.inventory.type)  # Creating filter
        filter.apply(input)                     # Apply filter to input
        fconfig = input.toString()              # Filtered config input

        return director.redirect(actor   = 'material_simulations/espresso/input-create',
                                routine = 'createRecord',
                                text    = fconfig,
                                id      = self.inventory.id,
                                taskid  = self.inventory.taskid,
                                type    = self.inventory.type,
                                subtype = self.inventory.subtype,
                                fname   = self.inventory.fname,
                                description = self.inventory.description)



    def __init__(self, name = None):
        actorname   = name
        if not name:    # No name, use default
            actorname    = "material_simulations/espresso-utils/generate-default"
        super(QEGenerator, self).__init__(name=actorname)


    def _configure(self):
        super(QEGenerator, self)._configure()
        self.id             = self.inventory.id
        self.simtype        = self.inventory.simtype
        self.structureid    = self.inventory.structureid

        self.taskid         = self.inventory.taskid
        self.type           = self.inventory.type
        self.subtype        = self.inventory.subtype

        self.fname          = self.inventory.fname
        self.description    = self.inventory.description
        self.text           = self.inventory.text
        self.linkorder      = self.inventory.linkorder


    def _init(self):
        super(QEGenerator, self)._init()



__date__ = "$Mar 26, 2010 12:00:39 PM$"


