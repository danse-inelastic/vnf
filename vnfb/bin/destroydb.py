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


## Destroy vnf db.
## This will remove all existing tables, so be careful!


from luban.applications.UIApp import UIApp as base


class DbApp(base):


    class Inventory(base.Inventory):

        import pyre.inventory

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", default='clerk')
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        force = pyre.inventory.bool(name='FORCE')
        force.meta['tip'] = "if true, the script won't prommpt user for permission"


    def main(self, *args, **kwds):
        msg = '\n\n'
        msg += '  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n'
        msg += '  !!! This is going to destroy the database !!!\n'
        msg += '  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n'
        msg += '\n'
        print msg

        force = self.inventory.force
        if not force:
            msg = ' * Are you really sure you want to do that !? (YeS/no) '
            response = raw_input(msg)
            if response != 'YeS':
                print 'exit'
                return
        
        clerk = self.clerk
        clerk.importAllDataObjects()

        clerk.db.destroyAllTables()
        return


    def __init__(self):
        base.__init__(self, 'destroydb')
        return


    def _getPrivateDepositoryLocations(self):
        from vnfb.deployment import pyre_depositories
        return pyre_depositories
    


def main():
    import journal
    journal.debug('db').activate()
    app = DbApp()
    return app.run()


if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
