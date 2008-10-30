#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



class Table:

    def __init__(self, column_descriptors, rows = None):

        self.column_descriptors = column_descriptors

        if rows is None: rows = []
        self.rows = rows
        return


    def identify(self, visitor):
        return visitor.onTable(self)


    def addRow(self, *row):
        self.rows.append( row )
        return



class ColumnDescriptor:

    def __init__(self, id, label, datatype, **kwds):
        self.id = id
        self.label = label
        self.datatype = datatype
        self.options = kwds
        return


def test():
    cols = [
        ColumnDescriptor( 'col1', 'Title', 'text' ),
        ColumnDescriptor( 'col2', 'Date', 'date', valid_range = [ '01/01/1977', '01/01/2008' ] ),
        ]
    table = Table( cols )
    table.addRow( 'abc', '06/06/2006' )
    table.addRow( 'hi', '05/05/2005' )
    return

if __name__ == '__main__': test()


# version
__id__ = "$Id$"

# End of file 
