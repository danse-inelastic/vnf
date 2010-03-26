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
from luban.content import select
from luban.content import load

from luban.components.AuthorizedActor import AuthorizedActor as base

# Requires simulation id,
class QEGenerator(base):

    class Inventory(base.Inventory):
        import pyre.inventory
        # Simulation attributes
        id          = pyre.inventory.str('id', default='')          # Simulation id
        # Task attributes
        taskid      = pyre.inventory.str('taskid', default='')      # Task id
        type        = pyre.inventory.str('type', default='')        # Task type
        # Input attributes
        fname       = pyre.inventory.str('fname', default='')
        description = pyre.inventory.str('description', default='')
        text        = pyre.inventory.str('text', default='')


    def default(self, director):
        return select(id='main-display-area').replaceContent(self.content(director))


    def content(self, director):
        "Populates the content for creation of input configuration"
        title   = "Create Input Configuration: %s" % self.type
        label   = "Select Option"
        return self._document(director, title, label)


    def _document(self, director, title, label):
        doc         = lc.document(title = title)
        splitter    = doc.splitter(orientation = "vertical")
        sA          = splitter.section()
        sB          = splitter.section()
        sA.add(self._viewIndicator(director, label))
        sB.add(self._setForm(director))

        return doc


    def _viewIndicator(self, director, label):
        path = []
        path.append(('Simulations ', load(actor='materialsimulation')))
        path.append(('Quantum Espresso ', load(actor='materialsimulation')))
        path.append(('%s ' % self.id, load(actor    = 'material_simulations/espresso/sim-view',
                                           id       = self.id)))
        path.append(('%s Task ' % self.type, load(actor    = 'material_simulations/espresso/task-view',
                                                  id       = self.id,
                                                  taskid   = self.taskid,
                                                  type     = self.type)))
        path.append(label)
        return director.retrieveVisual('view-indicator', path=path)


    def _setForm(self, director, visual = None):
        "Default implementation of input form"
        visual_     = "material_simulations/espresso/input-default"
        if visual:      # set visual if passed
            visual_ = visual

        return director.retrieveVisual(visual_,
                                       actor        = self.inventory,
                                       director     = director)


    def __init__(self, name = None):
        actorname   = name
        if not name:    # No name, use default
            actorname    = "material_simulations/espresso-utils/generate-default"
        super(QEGenerator, self).__init__(name=actorname)


    def _configure(self):
        super(QEGenerator, self)._configure()
        self.id             = self.inventory.id

        self.taskid         = self.inventory.taskid
        self.type           = self.inventory.type

        self.fname          = self.inventory.fname
        self.description    = self.inventory.description
        self.text           = self.inventory.text


    def _init(self):
        super(QEGenerator, self)._init()



__date__ = "$Mar 26, 2010 12:00:39 PM$"


