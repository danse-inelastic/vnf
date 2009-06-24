from vnf.components.Actor import Actor
from vnf.applications.WebApplication import AuthenticationError


class DirectDB(Actor):

    class Inventory(Actor.Inventory):

        import pyre.inventory

        encoder = pyre.inventory.str('encoder', default = 'json')

        format = pyre.inventory.str('format', default = 'dictionary')
        
        tables = pyre.inventory.str('tables')
        
        columns = pyre.inventory.str('columns', default = 'all')

        where = pyre.inventory.str('where')

        id = pyre.inventory.str('id')
        

    def get(self, director):
        # these next lines are a hack just to make sure the user is authenticated
        try:
            page = director.retrieveSecurePage( 'greet' )
        except AuthenticationError, error:
            return error.page

        if 'all' in self.columns:
            records = self._getRecords(director, self.tables, self.where)
            return self.encoder(records)
        else:
            results = self._getAttributes(director, self.tables, self.columns, self.where)
            return self.attributeEncoder(results)
    
#    def put(self, director, jsonFormattedInfo):
#        # these next lines are a hack just to make sure the user is authenticated
#        try:
#            page = director.retrieveSecurePage( 'greet' )
#        except AuthenticationError, error:
#            return error.page
#        
#        # assume the is a handler directive
#        
#        # if there's a file string, assume it is in json format
#        records = self._getRecords(director, self.tables, self.where)
#        return self.encoder(records)


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
                    where = "(%s) and (creator='%s' or creator='vnf')" % (where, director.sentry.username)
                else:
                    where = "(creator='%s' or creator='vnf')" % (director.sentry.username,)
    
            records = director.clerk.db.fetchall(table, where=where)
            results += records
        return results
    

    def _getAttributes(self, director, tables, columns, where):
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
                    if 'all' in where:
                        where=''
                    else:
                        where = "(%s) and (creator='%s' or creator='vnf')" % (where, director.sentry.username)
                else:
                    where = "(creator='%s' or creator='vnf')" % (director.sentry.username,)
    
            attributes = director.clerk.db.fetchAttributeFromAll(table, columns, where=where)
            attributes = flatten(attributes)
            results += attributes
        return results
    

    def _jsonEncoder(self, records):
        records = map(self._record2dict, records)
        import cjson
        # make sure all are encodable
        data=[]
        for r in records:
            #print r
            #note this will return either an *array* of json objects (which are dictionaries)
            # or an array of cifs...
            if 'dictionary' in self.format:
                for k,v in r.iteritems():
                    try:
                        cjson.encode(v)
                    except:
                        r[k] = str(v)
                data.append(r)
            elif 'cif' in self.format:
                # convert record to structure 
                from diffpy.Structure import Structure, Lattice, Atom
                import numpy as n
                fc = n.array(r['fractional_coordinates'])
                fc = fc.reshape((-1,3)) 
                fcList = fc.tolist()
                if fc.ndim==1: #this "fixes" the way tolist() works on single atoms or no atoms
                    fcList = [fcList]
                atomSymbols = r['atom_symbols']
                atoms = [Atom(s,c) for s,c in zip(atomSymbols,fcList)]
                lat = n.array(r['cartesian_lattice'])
                lat = lat.reshape((3,3))
                lat = lat.tolist()
                s = Structure( atoms, lattice = Lattice(base = lat))
                # expand the assymetric unit to generate all atoms in the unit cell?
                #?
                # convert structure to cif form
                data.append(s.writeStr('cif'))
        return cjson.encode(data)
    
    def _jsonAttributeEncoder(self, attributes):
        import cjson
        # make sure all are encodable
        data=[]
        for a in attributes:
            #print a
            #note this will return either an *array* of json-encoded attributes
            if 'dictionary' in self.format:
                try:
                    cjson.encode(a)
                except:
                    a = str(a)
                data.append(a)
            else:
                raise Exception
        return cjson.encode(data)


    def _record2dict(self, record):
        d = {}
        for col in record.getColumnNames():
            value = record.getColumnValue(col)
            d[col] = value
            continue
        return d
    
    
    def _configure(self):
        self.encoder = self._encoders[self.inventory.encoder]
        self.attributeEncoder = self._attributeEncoders[self.inventory.encoder]
        self.format = self.inventory.format
        
        # as a quick fix we simply hyphenate the tables if we want to query more than one
        self.tables = self.inventory.tables.split('-')
        
        id = self.inventory.id
        where = self.inventory.where
        if id and where:
            where = "(%s) and id='%s'" % (where, id)
        elif id:
            where = "id='%s'" % id
        self.where = where
        
        self.columns = self.inventory.columns
        return
    
    def getPotentialContents(self, director):
        # this method is a hack for gulpUi for now since it needs a potential which
        # is *associated* with gulppotentials metadata, rather than the metadata itself
        # Since going to change gulp into javascript eventually, little point in
        # altering this class significantly for now
        
        # these next lines are a hack just to make sure the user is authenticated
        try:
            page = director.retrieveSecurePage('greet')
        except AuthenticationError, error:
            return error.page

        # get the results
        records = self._getRecords(director, self.tables, self.where)
        # for now, assume the first potential is the "right" one, and get the potential name
        # (eventually this will have to be redone to search for a particular potential with a particular name)
        # (should change the name to be the primary key so it will reject it if it has the same name)
        potential = records[0]
        potentialName = records[0].potential_name
        #then read
        potentialPath = director.clerk.dds.abspath(potential, filename=potentialName)
        potentialContents = open(potentialPath).read()
        return potentialContents

    def __init__(self, name=None):
        if name is None:
            name = "directdb"
        super(DirectDB, self).__init__(name)

        # encoders
        self._encoders = {
            'json': self._jsonEncoder,
            }
        self._attributeEncoders = {
            'json': self._jsonAttributeEncoder,
            }
        
        return


    pass # end of DirectDB

def flatten(xList,whereto=1):
    """flattens a multidimensional list to a specified extent
    starting from the outer dimension"""
    temp1=xList
    while whereto>0:
        temp2=[]
        for x in temp1:
            temp2=temp2+list(x)
        temp1=temp2
        whereto=whereto-1
    return temp1
    