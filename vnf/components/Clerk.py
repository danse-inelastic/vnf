# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



def findClerks(extensions):
    s = 'from vnf.components.%s.Clerk import Clerk'
    def _(ext):
        exec s % ext in locals()
        return Clerk        
    return [ _(ext) for ext in extensions ]


def findDeepCopiers(extensions):
    s = 'from vnf.components.%s.Clerk import DeepCopier'
    def _(ext):
        exec s % ext in locals()
        return DeepCopier
    return [ _(ext) for ext in extensions ]


#from vnf.components import Undef
#from vnf.variables import Variable, LazyValue
#from vnf.SqlExpressions import (
#    Expr, Select, Insert, Update, Delete, Column, Count, Max, Min,
#    Avg, Sum, Eq, And, Asc, Desc, compile_python, compare_columns, SQLRaw,
#    Union, Except, Intersect, Alias, SetExpr)
from pyre.components.Component import Component

class Clerk(Component):


    class Inventory(Component.Inventory):

        import pyre.inventory
        
        # properties
        db = pyre.inventory.str(name='db', default='vnf')
        db.meta['tip'] = "the name of the database"

        dbwrapper = pyre.inventory.str(name='dbwrapper', default='psycopg')
        dbwrapper.meta['tip'] = "the python package that provides access to the database back end"

        


    def __init__(self, *args, **kwds):
        Component.__init__(self, *args, **kwds)
        return


    def indexUsers(self, where=None):
        """create an index of all users that meet the specified criteria"""
        from vnf.dom.User import User
        index = {}
        users = self.db.fetchall(User, where=where)
        for user in users:
            index[user.username] = user
            continue
        return index

    def indexActiveUsers(self):
        """create an index of all active users"""
        return self.indexUsers()
        return self.indexUsers(where="status='a'")

    def indexJobs(self, where = None):
        '''create and index all jobs'''
        from vnf.dom.Job import Job
        return self._index( Job, where )

    def indexInstruments(self, where = None):
        """create an index of all instruments
        that meet the specified criteria"""
        from vnf.dom.Instrument import Instrument
        return self._index( Instrument, where )

    def indexSampleAssemblies(self, where = None):
        """create an index of all sample assemblies
        that meet the specified criteria"""
        from vnf.dom.SampleAssembly import SampleAssembly
        return self._index( SampleAssembly, where )
    
    def indexSamples(self, where = None):
        '''create and index of all samples
        that meet the specified criteria'''
        from vnf.dom.Sample import Sample
        return self._index( Sample, where )

    def indexScatterers(self, where = None):
        '''create and index of all scatterers
        that meet the specified criteria'''
        from vnf.dom.Scatterer import Scatterer
        return self._index( Scatterer, where )

    def indexScatteringKernels(self, where = None):
        '''create and index of all scatterers
        that meet the specified criteria'''
        from vnf.dom.ScatteringKernel import ScatteringKernel
        from vnf.dom import subclassesOf
        tables = subclassesOf( ScatteringKernel )

        ret = {}
        for table in tables:
            temp = self._index( table, where )
            for id, record in temp.iteritems():
                ret[ (id, table) ] = record
                continue
            continue
        return ret

    def indexServers(self, where = None):
        '''create and index of all servers
        that meet the specified criteria'''

        from vnf.dom.Scatterer import Scatterer
        return self._index( Scatterer, where )


    def indexNeutronExperiments(self, where=None):
        director = self.director
        username = director.sentry.username
        from vnf.dom.NeutronExperiment import NeutronExperiment
        return self._index(NeutronExperiment, where=where)


    def getCrystal(self, id):
        '''retrieve crystal of given id'''
        from vnf.dom.Crystal import Crystal
        return self._getRecordByID( Crystal, id )

    
    def getJob(self, id):
        '''retrieve job of given id'''
        from vnf.dom.Job import Job
        return self._getRecordByID( Job, id )
    
    
    def getJobs(self, where = None):
        '''retrieve all jobs'''
        from vnf.dom.Job import Job
        return self._getAll( Job, where )
    
    
    def getSample(self, id):
        '''retrieve sample of given id'''
        from vnf.dom.Sample import Sample
        return self._getRecordByID( Sample, id )
    
    def getSamples(self, where = None):
        '''retrieve all samples'''
        from vnf.dom.Matter import Matter
        return self._getAll( Matter, where )

    def getSampleAssembly(self, id):
        '''retrieve sample assembly of given id'''
        from vnf.dom.SampleAssembly import SampleAssembly
        return self._getRecordByID( SampleAssembly, id )
    
#    def getScatteringKernels(self, where = None):
#        '''retrieve all scattering kernels'''
#        from vnf.dom.ScatteringKernel2 import ScatteringKernel2
#        return self._getAll( ScatteringKernel2, where )


    def getUser(self, username):
        '''retrieve user of given username'''
        from vnf.dom.User import User
        all = self.db.fetchall( User, where = "username='%s'" % username )
        assert len(all) == 1
        return all[0]
    
        
    def getInstrument(self, id):
        '''retrieve instrument of given id'''
        from vnf.dom.Instrument import Instrument
        return self._getRecordByID( Instrument, id )


    def getScatterer(self, id):
        '''retrieve scatterer of given id'''
        from vnf.dom.Scatterer import Scatterer
        return self._getRecordByID( Scatterer, id )

    
    def getServer(self, id):
        '''retrieve server of given id'''
        from vnf.dom.Server import Server
        return self._getRecordByID( Server, id )
    

    def getServers(self, where = None):
        '''retrieve all servers'''
        from vnf.dom.Server import Server
        return self._getAll( Server, where )


    def getNeutronExperiment(self, id):
        from vnf.dom.NeutronExperiment import NeutronExperiment
        return self._getRecordByID( NeutronExperiment, id )


    def getSampleEnvironment(self,id):
        from vnf.dom.SampleEnvironment import SampleEnvironment
        return self._getRecordByID( SampleEnvironment, id )


    def newInstrumentConfiguration(self, instrument):
        tablename = '%sconfiguration' % instrument.id
        try: table = self._getTable(tablename)
        except: table = self._getTable('instrumentconfigurations')

        # new configuration
        configuration = self.newOwnedObject(table)

        # set target
        configuration.target = instrument
        self.updateRecord(configuration)

        # copy the default configuration (the components)
        default = self.dereference(instrument.components)
        # to the configuration
        components = configuration.components
        for name, component in default:
            copy = self.duplicateRecord(component)
            components.add(copy, self.db, name=name)
            continue

        return configuration


    def duplicateRecord(self, record):
        save_id = record.id

        #new id
        director = self.director
        id = new_id(director)

        #give the record a new id
        record.id = id

        #save the new record
        new = self.newRecord(record)

        #restore
        record.id = save_id

        return self._getRecordByID(record.__class__, id)
    

    def updateRecord(self, record):
        id = record.id
        where = "id='%s'" % id
        
        assignments = []
        
        for column in record.getColumnNames():
            value = getattr( record, column )
            #value = _tostr( value )
            assignments.append( (column, value) )
            continue
        
        self.db.updateRow(record.__class__, assignments, where)
        return record


    def getRecordByID(self, tablename, id):
        Table = self._getTable(tablename)
        return self._getRecordByID(Table, id)
    
#    def find(self, cls_spec, *args, **kwargs):
#        """Perform a query.
#
#        Some examples::
#
#            clerk.find(Polycrystal, Polycrystal.chemical_formula == "KC28H") --> all Polycrystals with chemical formula KC28H
#            clerk.find(Person, chemical_formula == "KC28H") --> same
#
#        @param cls_spec: The class or tuple of classes whose
#            associated tables will be queried.
#        @param args: Instances of L{Expr}.
#        @param kwargs: Mapping of simple column names to values or
#            expressions to query for.
#
#        @return: A L{ResultSet} of instances C{cls_spec}. If C{cls_spec}
#            was a tuple, then an iterator of tuples of such instances.
#        """
#        if self._implicit_flush_block_count == 0:
#            self.flush()
#        find_spec = FindSpec(cls_spec)
#        where = get_where_for_args(args, kwargs, find_spec.default_cls)
#        return self._result_set_factory(self, find_spec, where)


    def newOwnedObject(self, table, owner = None):
        '''create a new record for the given table.

        The given table is assumed to have following fields:
          - id
          - creator
          - date
        '''
        if isinstance(table, str): table = self._getTable(table)
        
        director = self.director
        id = new_id( director )

        record = table()
        record.id = id

        if not owner: 
            owner = director.sentry.username
        record.creator = owner
        
        self.newRecord( record )
        return record


    def newDbObject(self, table):
        '''create a new record for the given table.

        The given table is assumed to have following fields:
          - id
        '''
        director = self.director
        
        record = table()
        
        id = new_id( director )
        record.id = id

        self.newRecord( record )
        return record


    def newRecord(self, record):
        'insert a new record into db'
        try:
            self.db.insertRow( record )
        except:
            columns = record.getColumnNames()
            values = [ record.getColumnValue( column ) for column in columns ]
            s = ','.join(
                [ '%s=%s' % (column, value)
                  for column, value in zip(columns, values)
                  ] )
            self._debug.log( 'failed to insert record: %s' % s)
            raise
        return record


    def deleteRecord(self, record, recursive=False):
        return self.referenceManager.deleteRecord(record, recursive=recursive)


    def dereference(self, pointer):
        '''dereference a "pointer"'''
        return pointer.dereference(self.db)


    def _referred(self, record):
        return self.referenceManager.referred(record)


    def _getTable(self, tablename):
        from vnf.dom.registry import tableRegistry as registry
        try: return registry.get(tablename)
        except KeyError:
            # backward compatibility
            candidate = tablename.lower() + 's'
            return registry.get(candidate)


    def _index(self, table, where = None):
        '''create a dictionary of {id: row} for the given table

        table: the table to be searched
        where: the searching criteria
        '''
        index = {}
        all = self.db.fetchall(table, where=where)
        for item in all:
            index[item.id] = item
        return index

    
    def _getAll(self, table, where = None):
        index = {}
        all = self.db.fetchall(table, where=where)
        return all

    
    def _getRecordByID(self, table, id ):
        all = self.db.fetchall( table, where = "id='%s'" % id )
        if len(all) == 1:
            return all[0]
        raise RuntimeError, "Cannot find record of id=%s in table %s" % (
            id, table.__name__)


    def _init(self):
        Component._init(self)

        # connect to the database
        import pyre.db
        dbkwds = DbAddressResolver().resolve(self.inventory.db)
        self.db = pyre.db.connect(wrapper=self.inventory.dbwrapper, **dbkwds)

        self.deepcopy = self.DeepCopier( self )

        from vnf.dom.ReferenceManager import ReferenceManager
        self.referenceManager = ReferenceManager(self.db)
        return

#class FindSpec(object):
#    """The set of tables or expressions in the result of L{Store.find}."""
#
#    def __init__(self, cls_spec):
#        self.is_tuple = type(cls_spec) == tuple
#        if not self.is_tuple:
#            cls_spec = (cls_spec,)
#
#        info = []
#        for item in cls_spec:
#            if isinstance(item, Expr):
#                info.append((True, item))
#            else:
#                info.append((False, get_cls_info(item)))
#        self._cls_spec_info = tuple(info)
#
#        # Do we have a single non-expression item here?
#        if not self.is_tuple and not info[0][0]:
#            self.default_cls = cls_spec[0]
#            self.default_cls_info = info[0][1]
#            self.default_order = self.default_cls_info.default_order
#        else:
#            self.default_cls = None
#            self.default_cls_info = None
#            self.default_order = Undef
#
#    def get_columns_and_tables(self):
#        columns = []
#        default_tables = []
#        for is_expr, info in self._cls_spec_info:
#            if is_expr:
#                columns.append(info)
#                if isinstance(info, Column):
#                    default_tables.append(info.table)
#            else:
#                columns.extend(info.columns)
#                default_tables.append(info.table)
#        return columns, default_tables
#
#    def is_compatible(self, find_spec):
#        """Return True if this FindSpec is compatible with a second one."""
#        if self.is_tuple != find_spec.is_tuple:
#            return False
#        if len(self._cls_spec_info) != len(find_spec._cls_spec_info):
#            return False
#        for (is_expr1, info1), (is_expr2, info2) in zip(
#            self._cls_spec_info, find_spec._cls_spec_info):
#            if is_expr1 != is_expr2:
#                return False
#            if info1 is not info2:
#                return False
#        return True
#
#    def load_objects(self, store, result, values):
#        objects = []
#        values_start = values_end = 0
#        for is_expr, info in self._cls_spec_info:
#            if is_expr:
#                values_end += 1
#                variable = getattr(info, "variable_factory", Variable)(
#                    value=values[values_start], from_db=True)
#                objects.append(variable.get())
#            else:
#                values_end += len(info.columns)
#                obj = store._load_object(info, result,
#                                         values[values_start:values_end])
#                objects.append(obj)
#            values_start = values_end
#        if self.is_tuple:
#            return tuple(objects)
#        else:
#            return objects[0]
#
#    def get_columns_and_values_for_item(self, item):
#        """Generate a comparison expression with the given item."""
#        if isinstance(item, tuple):
#            if not self.is_tuple:
#                raise TypeError("Find spec does not expect tuples.")
#        else:
#            if self.is_tuple:
#                raise TypeError("Find spec expects tuples.")
#            item = (item,)
#
#        columns = []
#        values = []
#        for (is_expr, info), value in zip(self._cls_spec_info, item):
#            if is_expr:
#                if not isinstance(value, (Expr, Variable)) and (
#                    value is not None):
#                    value = getattr(info, "variable_factory", Variable)(
#                        value=value)
#                columns.append(info)
#                values.append(value)
#            else:
#                obj_info = get_obj_info(value)
#                if obj_info.cls_info != info:
#                    raise TypeError("%r does not match %r" % (value, info))
#                columns.extend(info.primary_key)
#                values.extend(obj_info.primary_vars)
#        return columns, values
#
#
#def get_where_for_args(args, kwargs, cls=None):
#    equals = list(args)
#    if kwargs:
#        if cls is None:
#            raise Exception("Can't determine class that keyword "
#                               "arguments are associated with")
#        for key, value in kwargs.items():
#            equals.append(getattr(cls, key) == value)
#    if equals:
#        return And(*equals)
#    return Undef



class DbAddressResolver:
    
    def resolve(self, address):
        tmp = address.split('@')
        if len(tmp)==1:
            svr = tmp[0]
            up = ''
        elif len(tmp)==2:
            up,svr = tmp
        else:
            raise ValueError, 'Invalid db address: %r' % address

        host,port,database = self._resolve_svr(svr)
        user, pw = self._resolve_up(up)
        ret = {
            'database': database,
            }
        if host: ret['host'] = host
        if port: ret['port'] = port
        if user: ret['user'] = user
        if pw: ret['password'] = pw
        return ret
    

    def _resolve_up(self, up):
        separator = ':'
        tmp = up.split(separator)
        if len(tmp) == 1:
            user = tmp[0]
            if user == '': user = None
            pw = None
        elif len(tmp) == 2:
            user, pw = tmp
        else:
            raise ValueError, 'Invalid user, password: %r' % up
        return user, pw
    

    def _resolve_svr(self, svr):
        separator = ':'
        
        if svr.find(separator) == -1:
            # unix socket
            return None, None, svr
        splits = svr.split(separator)
        if len(splits)==2:
            host, database = splits
            # default port: 5432
            return host, 5432, database
        elif len(splits)==3:
            host, port, database = splits
            return host, port, database
        raise ValueError, 'Invalid db svr: %r' % (svr,)
    


class DeepCopier:

    def __init__(self, clerk):
        self.clerk = clerk
        self.director = clerk.director
        return


    def __call__(self, node):
        klass = node.__class__
        method = getattr(self, 'on%s' % klass.__name__)
        return method(node)


    def onSampleAssembly(self, sa):
        # a new container. empty
        from vnf.dom.SampleAssembly import SampleAssembly
        sa_copy = self.clerk.newOwnedObject( SampleAssembly )
        
        #first copy all scatterers
        scatterers = sa.scatterers
        self._copyReferenceSet( scatterers, sa_copy.scatterers )

        #then copy attributes
        self._copy_attrs( sa, sa_copy, attrs = ['short_description'] )

        # update record
        self.clerk.updateRecord( sa_copy )
        
        return sa_copy


    def onInstrument(self, instrument):
        # a new container. empty
        from vnf.dom.Instrument import Instrument
        instrument_copy = self.clerk.newOwnedObject( Instrument )

        #first copy all components
        components = sa.components
        self._copyReferenceSet( components, instrument_copy.components )

        #then copy attributes
        attrs = ['short_description', 'componentsequence', 'category']
        self._copy_attrs( sa, sa_copy, attrs = attrs )

        #copy geometer
        geometer = instrument.geometer
        self._copyGeometer( geometer, instrument_copy.geometer )

        #save
        self.clerk.updateRecord( instrument_copy )
        
        return instrument_copy


    def onScatterer(self, scatterer):
        #first make copies of shape and matter
        matter_copy = self._onreference( scatterer.matter )
        shape_copy = self._onreference( scatterer.shape )
        
        #now make a new record
        from vnf.dom.Scatterer import Scatterer as table
        scatterer_copy = self.clerk.newOwnedObject( table )
        
        #copy all kernels
        kernels = scatterer.kernels
        self._copyReferenceSet( kernels, scatterer_copy.kernels )

        #copy some attrs from old record
        attrs = ['short_description']
        self._copy_attrs( scatterer, scatterer_copy, attrs )

        #new record should point to the new matter and shape
        scatterer_copy.shape = shape_copy
        scatterer_copy.matter = matter_copy

        #update record to db
        self.clerk.updateRecord(scatterer_copy)
        return scatterer_copy


    def onBlock(self, block):
        return self._onRecordWithID( block )
    
    
    def onCylinder(self, cylinder):
        return self._onRecordWithID( cylinder )


    def onCrystal(self, crystal):
        return self._onRecordWithID( crystal )


    def onPolyCrystal(self, pc):
        return self._onRecordWithID( pc )


    def onDisordered(self, d):
        return self._onRecordWithID( d )


    def onMonochromaticSource(self, source):
        return self._onRecordWithID( source )


    def onDetectorSystem_fromXML(self, record):
        return self._onRecordWithID( record )


    def onAbInitio(self, record):
        return self._onRecordWithID( record )


    def _onreference(self, reference):
        record = reference.dereference(self.clerk.db)
        copy = self(record)
        newreference = reference.__class__( copy.id, copy.__class__ )
        return newreference


    def _onRecordWithID(self, record):
        # work with normal records with no reference, referenceset, etc
        from copy import copy
        newrecord = copy( record )
        newrecord.id = new_id( self.director )
        self.clerk.db.insertRow( newrecord )
        return newrecord


    def _copyReferenceSet(self, referenceset, newreferenceset):
        db = self.clerk.db
        elements = referenceset.dereference(db)
        for name, element in elements:
            elementcopy = self(element)
            newreferenceset.add( elementcopy, db, name = name )
            continue
        return


    def _copyGeometer(self, geometer, newgeometer):
        db = self.clerk.db
        registry = geometer.dereference()
        for k,v in registry.iteriterms():
            newgeometer.add( k, v.position, v.orientation, db, reference = v.reference)
            continue
        return 


    def _copy_attrs(self, old, new, attrs):
        for attr in attrs:
            setattr(new, attr, getattr(old, attr) )
            continue
        return

    pass # end of DeepCopier


def _tostr( value ):
    if isinstance( value, list ) or isinstance(value, tuple):
        ret =  '{%s}' % ','.join( [ str(item) for item in value ] )
        return ret
    return str(value)


from misc import new_id, empty_id

# version
__id__ = "$Id$"

# End of file 
