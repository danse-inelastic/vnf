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

from vnfb.utils.qeconst import SIMCHAINS
from vnfb.utils.qetaskcell import QETaskCell
from vnfb.utils.qegrid import QEGrid

import luban.content as lc
from luban.content.Splitter import Splitter
from luban.content.Paragraph import Paragraph
from luban.content import load
from luban.content.Link import Link


class QETasks:
    """Displays the chain of QE simulation steps"""

    def __init__(self, director, type, id = None):
        self._director  = director
        self._simtype   = type
        self._simlist   = self._getSimlist(type)


    def tasks(self, id):
        inputs          = self._director.clerk.getQEConfigurations(where="taskid='%s'" % id)
        orderedInputs   = self._orderInput(self._simlist, inputs)

        tasknum         = len(self._simlist)
        table           = QEGrid(lc.grid(Class="qe-tasks-table"))

        for i in range(tasknum):
            self._setTaskCell(table, i)
            # Special layout for action buttons (e.g. "Run Task")
            table.setCellStyle(2, i, "qe-action-task")

        return table.grid()


    def _setTaskCell(self, table, colnum):
        "Populates the task's cell"

        tc      = QETaskCell(self._simlist[colnum])
        rows    = (tc.header(), tc.taskInfo(), tc.action())
        table.addColumn(rows)

        

#
#            input   = orderedInputs[i]
#            #print input
#            if input:
#                link    = Link(label=input.filename,
#                               onclick=load(actor      = "material_simulations/espresso/input-view",
#                                            configid   = self._getId(self._simlist[i], inputs),
#                                            id         = id,
#                                            type       = self._simlist[i]  # ?
#                                            )
#                              )
#
#            section.add(link)
#
#            if i != listsize - 1:   # No arrow for last config
#                sep     = splitter.section()        # Separator
#                sep.add(Paragraph(text=" ----> "))


    def _orderInput(self, simlist, inputs):
        """Orders input according to simlist (E.g. simlist = ("PW", "PH") )"""
        newinputs   = []

        for name in simlist:
            newinputs.append(self._configObject(name, inputs))

        return newinputs


    def _configObject(self, type, inputs):
        """Returns object if simulation type exists or None otherwise"""
        for sim in inputs:
            if sim.type == type:
                return sim

        return None


    def _getSimlist(self, type):
        if type in SIMCHAINS:
            return SIMCHAINS[type]

        return ()


    def _getId(self, type, inputs):
        config  = self._configObject(type, inputs)
        if config:
            return config.id

        return ""

if __name__ == "__main__":
    pass


__date__ = "$Nov 9, 2009 10:50:54 AM$"


# *************** DEAD CODE ********************
#        one     = splitter.section()
#        one.add(Paragraph(text="PW "))
#        one.add(Link(label=filename, Class="action-link", onclick=load(actor="espresso/set-config", routine="link", id=id)))
#        sep     = splitter.section()        # Separator
#        sep.add(Paragraph(text=" -> "))
#        two     = splitter.section()
#        two.add(Paragraph(text="DOS"))
#        two.add(Link(label="Add"))


#    def _getActor(self, input):
#        # FIXME: merge to one 'input' actor
#        """Returns proper actor depending if 'input' exists"""
#        if input:   # View
#            return "material_simulations/espresso/input-view"
#
#        return "material_simulations/espresso/input-add" # Create New

