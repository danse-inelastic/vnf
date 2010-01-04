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
initialized database with data objects loaded
"""


from luban.applications.UIApp import UIApp as base


class DbApp(base):


    class Inventory(base.Inventory):

        import pyre.inventory

        table = pyre.inventory.str(name='table')
        tables = pyre.inventory.list(name='tables')
        

    def main(self, *args, **kwds):
        tables = self.inventory.tables
        if not tables:
            tables = [self.inventory.table]

        self.inittables(tables)
        return


    def inittables(self, tables):
        map(self.inittable, tables)


    def inittable(self, table):
        clerk = self.inventory.clerk
        orm = clerk.orm

        component = self.retrieveInitalizer(table)
        if hasattr(component, 'getObjects'):
            objs = component.getObjects()
            for obj in objs:
                orm.save(obj)

        elif hasattr(component, 'initdb'):
            component.initdb()

        else:
            raise RuntimeError

        return


    def retrieveInitalizer(self, name):
        component = self.retrieveComponent(name, factory='initdb', vault=['initdb'])
        if component is None:
            curator_dump = self._dumpCurator()
            raise RuntimeError, "could not locate db initializer %r. curator dump: %s" % (
                name, curator_dump)
        self.configureComponent(component)
        component.director = self
        return component


    def __init__(self):
        base.__init__(self, 'initdb')
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
