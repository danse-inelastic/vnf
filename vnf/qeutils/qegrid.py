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

class QEGrid:
    """
    QEGrid  - thin convenient wrapper for luban Grid.

    Notes:
        1. QEGrid basically consitst of two data structures:
           - grid that refers to the layout table (layout grid, or self._grid), and
           - grid that stores table rows and cells as a list data structure (data grid, or self._dgrid)
        - Can assign class styles only except in the constructor. Need to assign ids?
    """

    def __init__(self, grid):
        self._grid      = grid
        self._gridrows  = []    # holds rows of the grid
        self._dgrid     = []


    def addRow(self, columns, colclass = None):   #**kwds rowclass = None, rowid = None
        """Appends row to the table

        Parameters:
            columns - tuple of columns in the row
            rowclass - class applied to row
            colclass - tuple of classes applied to the column
        """

        (row, drow)  = self._addRow()   #**kwds
        for c in range(len(columns)):
            cell    = self._addCell(row, drow, self._getStyle(c, colclass))
            cell.add(columns[c])
            

    def addColumn(self, rows, rowclass = None):
        """Appends column to the table
        
        Parameters:
            rows     - tuple of rows in the column
            rowclass - class applied to row
        """
        if rows is None:
            return  # do nothing

        if len(self._gridrows) == 0:    # Rows do not exist, create first column
            self._addFirstColumn(len(rows))

        if len(self._gridrows) != len(rows):  # Row sizes do not match
            raise

        for r in range(len(rows)):
            cell    = self._addCell(self._gridrows[r],
                                    self._dgrid[r],
                                    self._getStyle(r, rowclass))
            cell.add(rows[r])
        

    def setCellStyle(self, row, col, cls = None, id = None):
        "Sets style for the cells (row, col)"
        # Check range
        if cls:                                     # class
            self._dgrid[row][col].Class    = cls

        if id:                                      # id
            self._dgrid[row][col].id        = id


    def setColumnStyle(self, col, cls):
        "Sets style for the column: col"
        # Note: No id because it can be assigned to a single element only
        for r in range(len(self._dgrid)):
            self._dgrid[r][col].Class    = cls


    def setRowStyle(self, row, cls = None, id = None):
        "Sets style for the row: row"
        if cls:                                     # class
            self._gridrows[row].Class   = cls

        if id:                                      # id
            self._gridrows[row].id      = id


    def setGridStyle(self, cls = None, id = None):
        "Sets style for the whole grid"
        if cls:
            self._grid.Class    = cls

        if id:
            self._grid.id       = id


    def createTable(self, rownum, colnum):
        """Create table's structure

        self._dgrid[m][n] - specifies the (m, n)-th cell
                          where m - row index, n - column index
        """
        for i in range(rownum):
            (row, drow)    = self._addRow()
            
            for j in range(colnum):
                self._addCell(row, drow)


    def grid(self):
        "Return layout grid (in case you need to use it for other purposes)"
        return self._grid


    def _addRow(self, **kwds):
        "Appends row to grid"
        row    = self._grid.row(**kwds) # layout row
        drow   = []                    # data row
        self._gridrows.append(row)
        self._dgrid.append(drow)
        return (row, drow)


    def _addFirstColumn(self, rownum):
        "Creates rows in the table, particularly useful for adding columns"
        for r in range(rownum):
            self._addRow()


    def _addCell(self, row, drow, cls = None):
        cell    = row.cell()
        if cls:
            cell.Class  = cls
        drow.append(cell)
        return cell


    def _getStyle(self, col, colclass):
        """Returns CSS class name if column number is less than the size of the class tuple
        or None otherwise"""

        if colclass is None:
            return None
        
        if len(colclass) < col:
            return None

        return colclass[col]


    def _inrange(self, ):
        pass

    def _listinrange(self):
        pass

__date__ = "$Dec 13, 2009 9:14:07 PM$"


