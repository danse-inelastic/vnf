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

        type = pyre.inventory.str(name='type')
        id = pyre.inventory.str(name='id')


    def main(self, *args, **kwds):
        clerk = self.inventory.clerk
        
        type = self.inventory.type
        type = clerk._getObjectByImportingFromDOM(type)
        id = self.inventory.id

        orm = clerk.orm
        obj = orm.load(type, id)
        records = orm._findAllOwnedRecords(obj)
        for r in records:
            print r.getTableName(), r.id
        return


    def __init__(self):
        base.__init__(self, 'findchildrenofdataobject')
        return


    def _defaults(self):
        super(DbApp, self)._defaults()
        from vnf.components.Clerk import Clerk
        self.inventory.clerk = Clerk()
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
