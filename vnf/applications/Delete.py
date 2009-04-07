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

class Delete(base):

    class Inventory(base.Inventory):

        import pyre.inventory
        id = pyre.inventory.str('id')
        table = pyre.inventory.str('table')
        recursive = pyre.inventory.bool('recursive')

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnf.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        debug = pyre.inventory.bool(name='debug', default=False)
        pass # end of Inventory
        

    def main(self):
        record = self.clerk.getRecordByID(self.table, self.id)
        self.clerk.deleteRecord(record, recursive = self.recursive)
        return


    def __init__(self, name='delete'):
        base.__init__(self, name)
        return


    def _configure(self):
        base._configure(self)

        self.id = self.inventory.id
        self.table = self.inventory.table
        self.recursive = self.inventory.recursive
        
        self.clerk = self.inventory.clerk
        self.clerk.director = self
        return


    def _init(self):
        base._init(self)

        # initialize table registry
        import vnf.dom
        vnf.dom.register_alltables()

        return



# version
__id__ = "$Id$"

# End of file 
