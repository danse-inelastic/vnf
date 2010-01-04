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



"""
create a data object and save it to the db
"""


from luban.applications.UIApp import UIApp as base


class DbApp(base):


    class Inventory(base.Inventory):

        import pyre.inventory

        type = pyre.inventory.str(name='type')


    def main(self, *args, **kwds):
        clerk = self.inventory.clerk
        
        type = self.inventory.type
        type = clerk._getObjectByImportingFromDOM(type)
        
        # assume the default constructor of the type can create a decent object
        obj = type()
        
        orm = clerk.orm
        orm.save(obj)
        return


    def __init__(self):
        base.__init__(self, 'createdataobject')
        return


    def _getPrivateDepositoryLocations(self):
        return ['../config', '../content/components', '/tmp/luban-services']



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
