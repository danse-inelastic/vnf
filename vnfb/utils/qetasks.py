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

import luban.content as lc
from luban.content.Splitter import Splitter
from luban.content.Paragraph import Paragraph
from luban.content import load
from luban.content.Link import Link


class QETasks:
    """Displays the chain of QE simulation steps"""

    def __init__(self, director, type=None):
        self._director  = director
        self._simtype   = type
        self._simlist   = self._getSimlist(type)


    def tasks(self, id):
        inputs          = self._director.clerk.getQEConfigurations(where="taskid='%s'" % id)
        orderedInputs   = self._orderInput(self._simlist, inputs)

        tasknum         = len(self._simlist)
        table           = self._setTable(tasknum)

        # Populate table
        for i in range(tasknum):
            self._setTaskCell(i)

        return table


    def _setTable(self, tasknum):
        table           = lc.grid(Class="qe-tasks-table")     #Splitter(orientation='horizontal')

        # self.cell[m][n] - specifies the (m, n)-th cell
        # m - row index, n - column index
        self.cell  = []

        # Create table structure
        for i in range(3):
            rows       = []
            row     = table.row()
            for j in range(tasknum):   # 3 columns
                rows.append(row.cell())

            self.cell.append(rows)

        return table


    def _setTaskCell(self, colnum):
        "Populates the task's cell"
        self.cell[0][colnum].add(Paragraph(text=self._simlist[colnum], Class="text-bold"))   # Simulation type
        self.cell[1][colnum].add(Paragraph(text="Input: ni.scf.in"))
        self.cell[2][colnum].add(Paragraph(text="Cancel"))

        link        = Link(label="Add",
                           onclick=load(actor      = "material_simulations/espresso/input-add",
                                        id         = id,
                                        type       = self._simlist[colnum])
                          )
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

