from vnf.components.Actor import Actor


class DirectDB(Actor):

    class Inventory(Actor.Inventory):

        import pyre.inventory

        encoder = pyre.inventory.str('encoder', default = 'json')

        #table = pyre.inventory.str('table')
        
        tables = pyre.inventory.str('tables')

        where = pyre.inventory.str('where')

        id = pyre.inventory.str('id')
        

    def get(self, director):
        # these next lines are a hack just to make sure the user is authenticated
        try:
            page = director.retrieveSecurePage( 'greet' )
        except AuthenticationError, error:
            return error.page

        records = self._getRecords(director, self.tables, self.where)
        return self.encoder(records)


    def _getRecords(self, director, tables, where):
        results=[]
        #print tables
        for table in tables:
            # should use acl mechanism to make sure users are authenticated to read
            # the tables and the records. this is a simple, naive implementation
            disallowed = ['user', 'users', 'registrant', 'registrants']
            if table.lower() in disallowed or table.lower().startswith('acl'):
                #print "Not allowed to access table %r" % table
                continue
            
            table = director.clerk._getTable(table)
            
            from vnf.dom.OwnedObject import OwnedObject
            if issubclass(table, OwnedObject):
                if where:
                    where = "(%s) and creator='%s'" % (where, director.sentry.username)
                else:
                    where = "creator='%s'" % (director.sentry.username,)
    
            records = director.clerk.db.fetchall(table, where=where)
            results+=records
        return results
    

    def _jsonEncoder(self, records):
        records = map(_record2dict, records)
        import cjson
        # make sure all are encodable
        for r in records:
            for k,v in r.iteritems():
                try:
                    cjson.encode(v)
                except:
                    r[k] = str(v)
        return cjson.encode(records)

    
    def _configure(self):
        self.encoder = self._encoders[self.inventory.encoder]
        
        # as a quick fix we simply hyphenate the tables if we want to query more than one
        self.tables = self.inventory.tables.split('-')
        
        id = self.inventory.id
        where = self.inventory.where
        if id and where:
            where = "(%s) and id='%s'" % (where, id)
        elif id:
            where = "id='%s'" % id
        self.where = where
        return


    def __init__(self, name=None):
        if name is None:
            name = "directdb"
        super(DirectDB, self).__init__(name)

        # encoders
        self._encoders = {
            'json': self._jsonEncoder,
            }

        return


    pass # end of DirectDB

def _record2dict(record):
    d = {}
    for col in record.getColumnNames():
        value = record.getColumnValue(col)
        d[col] = value
        continue
    return d