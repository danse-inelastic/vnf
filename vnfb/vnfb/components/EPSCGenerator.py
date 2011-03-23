# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import luban.content as lc
from luban.content import select, load

from luban.components.AuthorizedActor import AuthorizedActor as base

"""
EPSCGenerator - base actor class for EPSC generator pages

Notes:
    - Inventory for parameters is used in methods (e.g. self.inventory.id) to properly
    pass parameters with director.redirect()
"""

class EPSCGenerator(base):

    class Inventory(base.Inventory):
        import pyre.inventory
        # Simulation attributes
#        id          = pyre.inventory.str('id', default='')          # Simulation id
#        simtype     = pyre.inventory.str('simtype', default='')     # Simulation type
#        structureid = pyre.inventory.str('structureid', default='') # Atomic structure id
#        # Task attributes
#        taskid      = pyre.inventory.str('taskid', default='')      # Task id
        type        = pyre.inventory.str('type', default='')        # Task type
#        subtype     = pyre.inventory.str('subtype', default='')
#        # Input attributes
#        fname       = pyre.inventory.str('fname', default='')
#        description = pyre.inventory.str('description', default='')
        text        = pyre.inventory.str('text', default='')
#        linkorder   = pyre.inventory.str('linkorder', default='')   # Linkorder, if not set from qeconst.py


    def default(self, director):
        "Default routine"
        return select(id='main-display-area').replaceContent(self.content(director))


    def content(self, director):
        "Populates the content for creation of input configuration"
        title   = "Create Configuration"    #: %s" % self.type
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
#        self.id     = self.inventory.id
#        self.taskid = self.inventory.taskid
#        self.type   = self.inventory.type

        epsclink  = load( actor           = 'materialsimulation',
                        filter_key        = 'type',
                        filter_value      = 'epscsimulations')

        path = []
        path.append(('Simulations ',        load(actor='materialsimulation')))
        path.append(('EPSC', load(actor='material_simulations/epsc/sim-create')))
        path.append("Create Configuration")

#        path.append(('EPSC ',   epsclink))
#        path.append(('%s ' % self.id,       load(actor    = 'material_simulations/espresso/sim-view',
#                                                id       = self.id)))
#        path.append(('%s Task ' % self.type, load(actor    = 'material_simulations/espresso/task-view',
#                                                  id       = self.id,
#                                                  taskid   = self.taskid,
#                                                  type     = self.type)))
#        path.append(label)

        return director.retrieveVisual('view-indicator', path=path)


    def defaultForm(self, director, visual):
        "Default implementation of input form"
        visual_     = "material_simulations/epsc/input-default"
        if visual:      # set visual if passed
            visual_ = visual

        return director.retrieveVisual(visual_)#,
#                                       actor        = self.inventory,
#                                       director     = director,
#                                       simtype      = self.simtype,
#                                       structureid  = self.structureid)


    def __init__(self, name = None):
        actorname   = name
        if not name:    # No name, use default
            actorname    = "material_simulations/epsc-generators/generate-default"
        super(EPSCGenerator, self).__init__(name=actorname)


    def _configure(self):
        super(EPSCGenerator, self)._configure()

#        self.id             = self.inventory.id
#        self.simtype        = self.inventory.simtype
#        self.structureid    = self.inventory.structureid
#
#        self.taskid         = self.inventory.taskid
        self.type           = self.inventory.type
#        self.subtype        = self.inventory.subtype
#
#        self.fname          = self.inventory.fname
#        self.description    = self.inventory.description
        self.text           = self.inventory.text
#        self.linkorder      = self.inventory.linkorder


    def _init(self):
        super(EPSCGenerator, self)._init()

__date__ = "$Mar 22, 2011 8:01:27 PM$"


