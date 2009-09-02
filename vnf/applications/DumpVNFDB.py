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


from pyre.applications.Script import Script as base

class DumpVNFDB(base):

    class Inventory(base.Inventory):

        import pyre.inventory
        outdir = pyre.inventory.str('outdir')

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnf.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        pass # end of Inventory
        

    def main(self):
        db = self.clerk.db
        outdir = self.outdir
        
        from vnf.dom import alltables
        tables = alltables()

        from pyre.db import dump
        for table in tables:
            print ' * Dumping table %s' % table.name
            s = dump.dumps(db, table)
            path = os.path.join(outdir, table.name)
            open(path, 'w').write(s)
            continue
        
        return


    def _configure(self):
        base._configure(self)

        self.outdir = self.inventory.outdir

        self.clerk = self.inventory.clerk
        self.clerk.director = self
        return


    def _init(self):
        base._init(self)

        if os.path.exists(self.outdir):
            raise RuntimeError, '%s already exists' % self.outdir

        os.makedirs(self.outdir)

        # initialize table registry
        import vnf.dom
        vnf.dom.register_alltables()
        
        return


import os    

# version
__id__ = "$Id$"

# End of file 
