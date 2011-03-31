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


## This script is inherited from vnf-alpha, and it is good for initialization
## of db tables that are not mapped by dsaw.model orm.


## Initialize vnf db to have necessary tables. This will remove all
## existing tables, so be careful!


from pyre.applications.Script import Script


class DbApp(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", default='clerk')
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        import pyre.idd
        idd = pyre.inventory.facility('idd-session', factory=pyre.idd.session, args=['idd-session'])
        idd.meta['tip'] = "access to the token server"

        wwwuser = pyre.inventory.str(name='wwwuser', default='')

        tables = pyre.inventory.list(name='tables', default=[])
        ignoreTables = pyre.inventory.list(name='ignoreTables', default=[])

        init_tables = pyre.inventory.bool('init-tables', default=False)


    def main(self, *args, **kwds):

        self.db.autocommit(True)

        self.db.createSystemTables()

        tables = self.tables
        if not tables:
            from vnf.dom import alltables
            tables = alltables()
        else:
            tables = [self.clerk._getTable(t) for t in tables]
            
        for table in self.inventory.ignoreTables:
            tables = tables.remove(table)

        for table in tables:
            self.db.registerTable(table)
            continue

        self.db._sametadata.create_all()
##         for table in tables:
##             #self.dropTable( table )
##             self.createTable( table )
##             if self.wwwuser: self.enableWWWUser( table )
##             continue

        if self.init_tables:
            for table in tables:
                self.initTable( table )

        return


    def createTable(self, table):
        # create the component table
        print " -- creating table %r" % table.name
        try:
            self.db.createTable(table)
        except self.db.ProgrammingError, msg:
            print "    failed; table exists?"
            print msg
        else:
            print "    success"

        return


    def dropTable(self, table):
        print " -- dropping table %r" % table.name
        try:
            self.db.dropTable(table)
        except self.db.ProgrammingError:
            print "    failed; table doesn't exist?"
        else:
            print "    success"

        return


    def initTable(self, table):
        module = table.__module__
        m = __import__( module, {}, {}, [''] )
        inittable = m.__dict__.get( 'inittable' )
        if inittable is None: return
        print " -- Inialize table %r" % table.name
        try:
            inittable( self.db )
        except self.db.IntegrityError:
            print "    failed; records already exist?"
        else:
            print "    success"
            
        return


    def enableWWWUser(self, table):
        print " -- Enable www user %r for table %r" % (self.wwwuser, table.name)
        sql = 'grant all on table "%s" to "%s"' % (table.name, self.wwwuser)
        c = self.db.cursor()
        c.execute(sql)
        return


    def __init__(self):
        Script.__init__(self, 'initdb-alpha')
        self.db = None
        return


    def _configure(self):
        Script._configure(self)
        self.clerk = self.inventory.clerk
        self.clerk.director = self
        self.wwwuser = self.inventory.wwwuser
        self.tables = self.inventory.tables
        self.init_tables = self.inventory.init_tables
        return


    def _init(self):
        Script._init(self)

        self.db = self.clerk.db
        self.idd = self.inventory.idd

        # initialize table registry
        import vnf.dom
        vnf.dom.register_alltables()

        # id generator
        def guid(): return '%s' % self.idd.token().locator
        import vnf.dom
        vnf.dom.set_idgenerator( guid )
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
