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

from luban.content.Grid import Grid

class QEGrid(Grid):
    """
    QEGrid  - thin convenient wrapper for luban Grid.
    """

    def __init__(self, **kwds):
        super(QEGrid, self).__init__(**kwds)

    def addRow(self, columns, trclass = None, tdclass = None):
        """Adds row with two cells to the table

        Parameters:
            columns - tuple of columns in the row
            trclass - class applied to row
            tdclass - tupple of classes applied to the column
        """
        row     = table.row()
        cell    = row.cell(Class="qe-cell-param")
        cell.add(first)
        cell    = row.cell(Class="qe-cell-value")
        cell.add(second)

    def setTable(self, rownum, colnum):
        pass

__date__ = "$Dec 13, 2009 9:14:07 PM$"


