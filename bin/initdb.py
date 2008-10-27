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

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnf.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        import pyre.idd
        idd = pyre.inventory.facility('idd-session', factory=pyre.idd.session, args=['idd-session'])
        idd.meta['tip'] = "access to the token server"


    def main(self, *args, **kwds):

        self.db.autocommit(True)

        from vnf.dom import alltables
        tables = alltables()

        for table in tables:
            #self.dropTable( table )
            self.createTable( table )
            continue

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


    def __init__(self):
        Script.__init__(self, 'initdb')
        self.db = None
        return


    def _configure(self):
        Script._configure(self)
        self.clerk = self.inventory.clerk
        self.clerk.director = self
        return


    def _init(self):
        Script._init(self)

        self.db = self.clerk.db

        self.idd = self.inventory.idd

        def guid(): return '%s' % self.idd.token().locator
        import vnf.dom
        vnf.dom.set_idgenerator( guid )
        return


    def _getPrivateDepositoryLocations(self):
        return ['../config']
    

from vnf.DbAddressResolver import DbAddressResolver


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
