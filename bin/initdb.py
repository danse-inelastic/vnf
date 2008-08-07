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
        

    def main(self, *args, **kwds):
        print "database:", self.inventory.db
        print "database manager:", self.db

        self.db.autocommit(True)

        from vnf.dom import alltables
        tables = alltables()

        for table in tables:
            self.createTable( table )
            self.enablewww( table )
        
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
        cmd = 'GRANT ALL ON %s TO %s' % (name, self.wwwusername)
        c = self.db.cursor()
        print cmd
        c.execute( cmd )
        return


    def __init__(self):
        Script.__init__(self, 'db')
        self.db = None
        return


    def _init(self):
        Script._init(self)

        import pyre.db
        dbname = self.inventory.db
        dbengine = self.inventory.dbengine
        self.db = pyre.db.connect(dbname, wrapper = dbengine)

        self.wwwusername = self.inventory.wwwusername
        return


def main():
    app = DbApp()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
