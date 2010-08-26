# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from vnfb.dom.QESetting import QESetting
from vnfb.qeutils.qegrid import QEGrid
from luban.content.FormSelectorField import FormSelectorField
from luban.content import select

from vnfb.qeutils.qeconst import SETTINGS, PROCESSORS, NOPARALSIM, SIMTYPE, OPT_DEFAULT
from vnfb.qeutils.qeconst import ID_SELECTOR_CORES
from vnfb.qeutils.qeutils import serverName
from vnfb.utils.serverlist import ServerList

import luban.content as lc
from luban.components.AuthorizedActor import AuthorizedActor as base

class Actor(base):

    class Inventory(base.Inventory):
        import pyre.inventory
        id          = pyre.inventory.str('id', default='')
        type        = pyre.inventory.str('type', default='')
        server      = pyre.inventory.str('server', default='')
        sname       = pyre.inventory.str('sname', default='')
        description = pyre.inventory.str('description', default='') # Not used
        numproc     = pyre.inventory.int('numproc', default=1)
        localdisk   = pyre.inventory.bool('localdisk', default=False)


    def default(self, director):
        return select(id='main-display-area').replaceContent(self.content(director))


    def setCoresList(self, director):
        "Sets cores list depending on server selection"
        procfield   = "Hello"
        return select(id=ID_SELECTOR_CORES).replaceContent(procfield)


    def _selectorCores(self, servlist):
        cores           = lc.document(id=ID_SELECTOR_CORES)
        procfield       = FormSelectorField(name="numproc", entries = self._procOptions(servlist, 0))
        cores.add(procfield)
        return cores


    def _optLevel(self):
        """
        Returns optimization level depending on 'scratch space' checkbox
            0 - NFS file system
            1 - Scratch space (local disk on each node)
        """
        if self.localdisk:
            return 1

        return 0


    def _procOptions(self, servlist, servorder):
        "Available options for number of cores"
        DEFAULT     = enumerate((1,))

        # servorder is out of range
        if not servorder in range(len(servlist)):
            return DEFAULT

        servname    = servlist[servorder]
        shortname   = serverName(servname)
        DEFAULT     = enumerate(PROCESSORS[shortname])

        for k in SIMTYPE.keys():
            if SIMTYPE[k] == self.type and k in NOPARALSIM:
                return enumerate((1,))  # Single core

        return DEFAULT


    def _sname(self):
        # Settings name is not set
        if self.sname == '':
            return "settings.conf"

        return self.sname


    def __init__(self, name):
        super(Actor, self).__init__(name=name)

        return


    def _configure(self):
        super(Actor, self)._configure()
        self.id             = self.inventory.id
        self.type           = self.inventory.type
        self.sname          = self.inventory.sname
        self.server         = self.inventory.server
        self.description    = self.inventory.description
        self.numproc        = self.inventory.numproc
        self.localdisk      = self.inventory.localdisk


    def _init(self):
        super(Actor, self)._init()
        return


__date__ = "$Aug 24, 2010 5:55:46 PM$"


