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



from pyre.applications.Script import Script


class DbApp(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        db = pyre.inventory.str('db', default='vnf')
        db.meta['tip'] = 'the database to connect to'

        dbengine = pyre.inventory.str('dbengine', default = 'psycopg2')

        wwwusername = pyre.inventory.str( 'wwwusername', default = '_www')
        wwwusername.meta['tip'] = 'user name of the apache server'
        
        import pyre.idd
        idd = pyre.inventory.facility('idd-session', factory=pyre.idd.session, args=['idd-session'])
        idd.meta['tip'] = "access to the token server"


    def main(self, *args, **kwds):
        print "database:", self.inventory.db
        print "database manager:", self.db

        self.db.autocommit(True)

        from vnf.dom import alltables
        tables = alltables()

        for table in tables:
            self.dropTable( table )
            self.createTable( table )
            self.enablewww( table )

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


    def enablewww(self, table):
        name = table.name
        cmd = 'GRANT ALL ON %s TO "%s"' % (name, self.wwwusername)
        c = self.db.cursor()
        #print cmd
        print " -- Grant user %r access to table %r" % (self.wwwusername, name)
        c.execute( cmd )
        return


    def initTable(self, table):
        module = table.__module__
        m = __import__( module, {}, {}, [''] )
        inittable = m.__dict__.get( 'inittable' )
        if inittable is None: return
        print " -- Inialize table %r" % table.name
        inittable( self.db )
        return


    def __init__(self):
        Script.__init__(self, 'initdb')
        self.db = None
        return


    def _init(self):
        Script._init(self)

        import pyre.db
        dbname = self.inventory.db
        dbengine = self.inventory.dbengine
        self.db = pyre.db.connect(dbname, wrapper = dbengine)

        self.wwwusername = self.inventory.wwwusername
        self.idd = self.inventory.idd

        def guid(): return '%s' % self.idd.token().locator
        import vnf.dom
        vnf.dom.set_idgenerator( guid )
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
