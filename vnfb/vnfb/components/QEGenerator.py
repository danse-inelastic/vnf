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

from vnfb.qeutils.qeconst import TYPE

import luban.content as lc
from luban.content import select
from luban.content import load

from luban.components.AuthorizedActor import AuthorizedActor as base

# Requires simulation id,
class Actor(base):

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
        doc         = lc.document(title   = "Create Input Configuration: %s" % self.type)
        splitter    = doc.splitter(orientation="vertical")
        sA          = splitter.section()
        sB          = splitter.section()
        sA.add(self._viewIndicator(director))
        sB.add(self._setForm(director))

        return doc


    def _viewIndicator(self, director):
        path = []
        path.append(('Simulations ', load(actor='materialsimulation')))
        path.append(('Quantum Espresso ', load(actor='materialsimulation')))
        path.append(('%s ' % self.id, load(actor    = 'material_simulations/espresso/sim-view',
                                           id       = self.id)))
        path.append(('%s Task ' % self.type, load(actor    = 'material_simulations/espresso/task-view',
                                                  id       = self.id,
                                                  taskid   = self.taskid,
                                                  type     = self.type)))
        path.append('Select Option')

        return director.retrieveVisual('view-indicator', path=path)


    #XXX: Consider special case for PW2
    def _setForm(self, director):
        "Default implementation of input form"
        visual  = "material_simulations/espresso/input-default"

        return director.retrieveVisual(visual,
                                       actor        = self.inventory,
                                       director     = director)


    def __init__(self, name):
        actorname   = name
        if not name:
            actorname    = "material_simulations/espresso-utils/generate-default"
        super(Actor, self).__init__(name=actorname)


    def _configure(self):
        super(Actor, self)._configure()
        self.id             = self.inventory.id

        self.taskid         = self.inventory.taskid
        self.type           = self.inventory.type

        self.fname          = self.inventory.fname
        self.description    = self.inventory.description
        self.text           = self.inventory.text


    def _init(self):
        super(Actor, self)._init()
        return

def actor():
    return Actor()


__date__ = "$Mar 26, 2010 12:00:39 PM$"


