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


from pyre.db.Table import Table

class User(Table):
    
    name = "users"
    
    import pyre.db
    
    id = pyre.db.varchar(name="id", length=30)
    id.meta['tip'] = "the user's id"
    id.constraints = "PRIMARY KEY"

    username = pyre.db.varchar(name='username', length=30)
    username.meta['tip'] = "the user's name"
    
    password = pyre.db.varchar(name="password", length=30)
    password.meta['tip'] = "the user's password"

    
class Group(Table):

    name = "groups"

    import pyre.db

    id = pyre.db.varchar(name="id", length=30)
    id.constraints = "PRIMARY KEY"

    import vnf.dom
    users = vnf.dom.referenceSet( name = 'users' )


from vnf.dom.registry import tableRegistry
tableRegistry.register( User )
tableRegistry.register( Group )


def idgenerator():
    global _id
    _id += 1
    return str(_id)
_id = 0
import vnf.dom
vnf.dom.set_referencesettable_idgenerator( idgenerator )


from pyre.applications.Script import Script


class DbApp(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        db = pyre.inventory.str('db', default='testdb')
        db.meta['tip'] = 'the database to connect to'

        wipe = pyre.inventory.bool('wipe', default=True)
        wipe.meta['tip'] = 'delete the table before inserting data?'

        create = pyre.inventory.bool('create', default=True)
        create.meta['tip'] = 'create the table before inserting data?'

        dbengine = pyre.inventory.str('dbengine', default = 'psycopg2')
        

    def main(self, *args, **kwds):
        print "database:", self.inventory.db
        print "database manager:", self.db

        self.db.autocommit(True)

        tables = [ User, Group ]
        from vnf.dom._referenceset import _ReferenceTable
        tables.append( _ReferenceTable )
        
        if self.inventory.wipe:
            for t in tables: self.dropTable( t )

        if self.inventory.wipe or self.inventory.create:
            for t in tables: self.createTable( t )

        #try:
        #    vnf.dom.create_referenceset_table( self.db )
        #except:
        #    pass
        
        # create user records
        user1 = User()
        user1.id = '0'
        user1.username = "aivazis"
        user1.password = "mga4demo"

        user2 = User()
        user2.id = '1'
        user2.username = 'demo'
        user2.password = 'demo'

        # store them in the database
        for record in [user1, user2]: self.save(record)

        # now extract all records and print them
        self.retrieve(User)

        
        # create a group record
        group = Group()

        users = group.users
        print 'referenceset instance: %s' % users
        print 'users: %s' % (users.dereference( self.db ), )

        print '> add one user' 
        users.add( [user1], self.db )
        print '  users: %s' % (users.dereference( self.db ), )

        print '> delete one use'
        users.delete( user1, self.db )
        print '  users: %s' % (users.dereference( self.db ), )

        print '> add two users'
        users.add( [user1, user2], self.db )
        print '  users: %s' % (users.dereference( self.db ), )

        print '> remove all users'
        users.clear( self.db )
        print '  users: %s' % (users.dereference( self.db ), )
        return


    def retrieve(self, table):
        print " -- retrieving from table %r" % table.name
        try:
            records = self.db.fetchall(table)
        except self.db.ProgrammingError, msg:
            print "    retrieve failed:", msg
            return
        else:
            print "    success"

        index = 0
        print records
        for record in records:
            index += 1
            columns = record.getColumnNames()
            s = [ '%s=%s' % (col, record.getColumnValue(col)) for col in columns ]
            s = ', '.join( s )
            print "record %d: %s" % (index, s)

        return records


    def save(self, item):
        print " -- saving into table %r" % item.name
        try:
            self.db.insertRow(item)
        except self.db.ProgrammingError, msg:
            print "    insert failed:", msg
        else:
            print "    success"

        return


    def createTable(self, table):
        # create the user table
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
        # drop the user table
        print " -- dropping table %r" % table.name
        try:
            self.db.dropTable(table)
        except self.db.ProgrammingError:
            print "    failed; table doesn't exist?"
        else:
            print "    success"

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

        return


def main():
    app = DbApp()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id: db.py,v 1.1.1.1 2006-11-27 00:10:10 aivazis Exp $"

# End of file 
