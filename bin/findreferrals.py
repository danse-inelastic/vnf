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


# find all objects that referred to the given data object


from luban.applications.UIApp import UIApp as base


class DbApp(base):


    class Inventory(base.Inventory):

        import pyre.inventory

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", default='clerk')
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        type = pyre.inventory.str(name='type')
        id = pyre.inventory.str(name='id')


    def main(self, *args, **kwds):
        clerk = self.inventory.clerk
        clerk.importAllDataObjects()
        
        type = self.inventory.type
        id = self.inventory.id
        orm = clerk.orm
        
        #         type = clerk._getObjectByImportingFromDOM(type)
        #         obj = orm.load(type, id)
        #         Obj = obj.__class__
        #         Table = orm(Obj)
        #         record = orm(obj)
        Table = clerk._getTable(type)
        
        record = clerk.db.query(Table).filter_by(id=id).one()

        from vnf.utils.db.findreferrals import findreferrals
        for r, desc in findreferrals(record, clerk):
            print '-', desc
        return


    def __init__(self):
        base.__init__(self, 'findreferrals')
        return


    def _getPrivateDepositoryLocations(self):
        from vnf.deployment import pyre_depositories
        return pyre_depositories



def main():
    import journal
    journal.debug('db').activate()
    journal.debug('db.findreferrals').activate()
    app = DbApp()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
