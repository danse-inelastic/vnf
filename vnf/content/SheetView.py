#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from praxis.tabular.SheetView import SheetView as base

class SheetView(base):

    def render(self, columns):
        """Render the view"""
        if self.model is None:
            raise self.ViewError(self, msg="no model is attached to this view")

        from Table import Table, ColumnDescriptor
        descriptors = [ _descriptor(col, self.columns) for col in columns ]
        table = Table(descriptors)
        
        #print "view %r of model %r" % (self.name, self.model.name)
        
        for row in self._sortedRows():
            values = []
            for column in columns:
                # get the cell value
                value, decorator = self.getCell(row, column)
                #values.append(self.formatter.format(decorator, value))
                values.append(value)
                continue
            table.addRow(*values)
            continue
        
        return table


def _descriptor(name, columns):
    col = columns[name]
    from Table import ColumnDescriptor
    label = col.label or name
    return ColumnDescriptor(label, label, _typename(col.type))


def _typename(type):
    from praxis.types.Currency import Currency
    if isinstance(type, Currency): return 'money'
    #from praxis.types.Float import Float
    #if isinstance(type, Float): return 'float'
    return 'text'


# version
__id__ = "$Id$"

# End of file 
