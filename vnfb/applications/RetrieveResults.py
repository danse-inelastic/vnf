#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2008  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from luban.applications.UIApp import UIApp as base

class RetrieveResults(base):
    
    class Inventory(base.Inventory):
        
        import pyre.inventory
        id = pyre.inventory.str('id')
        type = pyre.inventory.str('type')
        
        pass # end of Inventory
        

    def main(self):
        domaccess = self._domacces()
        
        id = self.id
        type = self.type
        computation = domaccess.getRecordByID(type, id)

        from vnfb.utils.computation import retrieve_results
        retrieve_results(computation, director=self)
        return


    def _domacces(self):
        domaccess = self.retrieveDOMAccessor('computation')
        # insure orm is enabled
        orm = domaccess.orm
        return domaccess


    def _configure(self):
        super(RetrieveResults, self)._configure()
        self.id = self.inventory.id
        self.type = self.inventory.type
        return


# version
__id__ = "$Id$"

# End of file 
