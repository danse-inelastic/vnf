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


from luban.applications.UIApp import UIApp as base


class DbApp(base):


    class Inventory(base.Inventory):

        import pyre.inventory

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", default='clerk')
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        type = pyre.inventory.str(name='type')
        id = pyre.inventory.str(name='id')
        ids = pyre.inventory.list(name='ids')


    def main(self, *args, **kwds):
        clerk = self.inventory.clerk
        
        type = self.inventory.type
        type = clerk._getObjectByImportingFromDOM(type)

        ids = self.inventory.ids
        if not ids:
            ids = [self.inventory.id]

        orm = clerk.orm
        for id in ids:
            obj = orm.load(type, id)
            orm.destroy(obj)
        return


    def __init__(self):
        base.__init__(self, 'destroydataobject')
        return


    def _getPrivateDepositoryLocations(self):
        return ['../config']



def main():
    import journal
    journal.debug('db').activate()
    app = DbApp()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
