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

class Component(Table):
    
    name = "components"
    
    import pyre.db
    
    id = pyre.db.varchar(name="id", length=30)
    id.meta['tip'] = "the component's id"
    id.constraints = "PRIMARY KEY"

    componentname = pyre.db.varchar(name='componentname', length=30)
    componentname.meta['tip'] = "the component's name"
    

    
class Composite(Table):

    name = "composites"

    import pyre.db

    id = pyre.db.varchar(name="id", length=30)
    id.constraints = "PRIMARY KEY"

    import vnf.dom
    components = vnf.dom.referenceSet( name = 'components' )

    geometer = vnf.dom.geometer( )



from vnf.dom.registry import tableRegistry
tableRegistry.register( Component )
tableRegistry.register( Composite )


def idgenerator():
    global _id
    _id += 1
    return str(_id)
_id = 0
import vnf.dom
vnf.dom.set_idgenerator( idgenerator )


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

        tables = [ Component, Composite ]
        from vnf.dom._hidden_tables import tables as _tables
        tables += _tables()
        
        if self.inventory.wipe:
            for t in tables: self.dropTable( t )

        if self.inventory.wipe or self.inventory.create:
            for t in tables: self.createTable( t )

        #try:
        #    vnf.dom.create_referenceset_table( self.db )
        #except:
        #    pass
        
        # create component records
        component1 = Component()
        component1.id = '0'
        component1.componentname = "moderator"

        component2 = Component()
        component2.id = '1'
        component2.componentname = 't0chopper'

        # store them in the database
        for record in [component1, component2]: self.save(record)

        # now extract all records and print them
        self.retrieve(Component)

        
        # create a composite record
        composite = Composite()

        components = composite.components
        print 'referenceset instance: %s' % components

        print '> add two components'
        components.add( component1, self.db, name = 'moderator' )
        components.add( component2, self.db, name = 't0chopper' )
        print '  components: %s' % (components.dereference( self.db ), )

        print 'register position and orientation of components'
        geometer = composite.geometer
        geometer.register( 'moderator', (0,0,0), (0,0,0), self.db )
        geometer.register( 't0chopper', (0,0,1), (0,0,0), self.db )

        reg = geometer.dereference( self.db )
        print [ (k, v.position, v.orientation) for k,v in reg.iteritems() ]
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
