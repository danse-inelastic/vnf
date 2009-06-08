#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                     (C) 2007-2009  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.applications.Script import Script as base

class FindDanglingReferences(base):

    class Inventory(base.Inventory):

        import pyre.inventory

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnf.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        debug = pyre.inventory.bool(name='debug', default=False)

        tables = pyre.inventory.list(name='tables', default=[])
        
        pass # end of Inventory
        

    def main(self):
        tables = self.tables
        def p(s): print s
        refs = self.clerk.referenceManager.findDanglingReferences(
            printer=p, tables=self.tables)
        for ref, record in refs:
            print 'reference %s, referred to by %r' % (ref, _str(record))
        return


    def __init__(self, name='find-dangling-references'):
        base.__init__(self, name)
        return


    def _configure(self):
        base._configure(self)

        self.clerk = self.inventory.clerk
        self.clerk.director = self

        self.tables = self.inventory.tables
        return


    def _init(self):
        base._init(self)

        # initialize table registry
        import vnf.dom
        vnf.dom.register_alltables()
        
        #
        tables = self.tables
        self.tables = [self.clerk._getTable(table) for table in tables]
        
        return



def _str(record):
    l = [ '%s=%s' % (col, record.getColumnValue(col))
          for col in record.getColumnNames()]
    return record.name + '(' + ', '.join(l) + ')'
        

# version
__id__ = "$Id$"

# End of file 
