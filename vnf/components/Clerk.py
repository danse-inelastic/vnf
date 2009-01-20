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


from vnf.components import Undef
from vnf.components.variables import Variable, LazyValue
from vnf.components.expr import (Expr, Select, Insert, Update, Delete, Column, Count, Max, Min,
    Avg, Sum, Eq, And, Asc, Desc, compile_python, compare_columns, SQLRaw,
    Union, Except, Intersect, Alias, SetExpr)
from vnf.components.exceptions import (
    WrongStoreError, NotFlushedError, OrderLoopError, UnorderedError,
    NotOneError, FeatureError, CompileError, LostObjectError, ClassInfoError)
from vnf.components.info import get_cls_info, get_obj_info
from pyre.components.Component import Component

class Clerk(Component):

    class Inventory(Component.Inventory):

        import pyre.inventory
        
        # properties
        db = pyre.inventory.str(name='db', default='vnf')
        db.meta['tip'] = "the name of the database"

        dbwrapper = pyre.inventory.str(name='dbwrapper', default='psycopg')
        dbwrapper.meta['tip'] = "the python package that provides access to the database back end"

    _result_set_factory = None

    def __init__(self, *args, **kwds):
        Component.__init__(self, *args, **kwds)
        self._implicit_flush_block_count = 0

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
    
    def find(self, cls_spec, *args, **kwargs):
        """Perform a query.

        Some examples::

            clerk.find(Polycrystal, Polycrystal.chemical_formula == "KC28H") --> all Polycrystals with chemical formula KC28H
            clerk.find(Polycrystal, chemical_formula == "KC28H") --> same

        @param cls_spec: The class or tuple of classes whose
            associated tables will be queried.
        @param args: Instances of L{Expr}.
        @param kwargs: Mapping of simple column names to values or
            expressions to query for.

        @return: A L{ResultSet} of instances C{cls_spec}. If C{cls_spec}
            was a tuple, then an iterator of tuples of such instances.
        """
#        if self._implicit_flush_block_count == 0:
#            self.flush()
        find_spec = FindSpec(cls_spec)
        where = get_where_for_args(args, kwargs, find_spec.default_cls)
        return self._result_set_factory(self, find_spec, where)


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

class ResultSet(object):
    """The representation of the results of a query.

    Note that having an instance of this class does not indicate that
    a database query has necessarily been made. Database queries are
    put off until absolutely necessary.

    Generally these should not be constructed directly, but instead
    retrieved from calls to L{Store.find}.
    """
    def __init__(self, store, find_spec,
                 where=Undef, tables=Undef, select=Undef):
        self._store = store
        self._find_spec = find_spec
        self._where = where
        self._tables = tables
        self._select = select
        self._order_by = find_spec.default_order
        self._offset = Undef
        self._limit = Undef
        self._distinct = False
        self._group_by = Undef
        self._having = Undef

    def copy(self):
        """Return a copy of this ResultSet object, with the same configuration.
        """
        result_set = object.__new__(self.__class__)
        result_set.__dict__.update(self.__dict__)
        return result_set

    def config(self, distinct=None, offset=None, limit=None):
        """Configure this result object in-place. All parameters are optional.

        @param distinct: Boolean enabling/disabling usage of the DISTINCT
            keyword in the query made.
        @param offset: Offset where results will start to be retrieved
            from the result set.
        @param limit: Limit the number of objects retrieved from the
            result set.

        @return: self (not a copy).
        """

        if distinct is not None:
            self._distinct = distinct
        if offset is not None:
            self._offset = offset
        if limit is not None:
            self._limit = limit
        return self

    def _get_select(self):
        if self._select is not Undef:
            if self._order_by is not Undef:
                self._select.order_by = self._order_by
            if self._limit is not Undef: # XXX UNTESTED!
                self._select.limit = self._limit
            if self._offset is not Undef: # XXX UNTESTED!
                self._select.offset = self._offset
            return self._select
        columns, default_tables = self._find_spec.get_columns_and_tables()
        return Select(columns, self._where, self._tables, default_tables,
                      self._order_by, offset=self._offset, limit=self._limit,
                      distinct=self._distinct, group_by=self._group_by,
                      having=self._having)

    def _load_objects(self, result, values):
        return self._find_spec.load_objects(self._store, result, values)

    def __iter__(self):
        """Iterate the results of the query.
        """
        result = self._store._connection.execute(self._get_select())
        for values in result:
            yield self._load_objects(result, values)

    def __getitem__(self, index):
        """Get an individual item by offset, or a range of items by slice.

        If a slice is used, a new L{ResultSet} will be return
        appropriately modified with OFFSET and LIMIT clauses.
        """
        if isinstance(index, (int, long)):
            if index == 0:
                result_set = self
            else:
                if self._offset is not Undef:
                    index += self._offset
                result_set = self.copy()
                result_set.config(offset=index, limit=1)
            obj = result_set.any()
            if obj is None:
                raise IndexError("Index out of range")
            return obj

        if not isinstance(index, slice):
            raise IndexError("Can't index ResultSets with %r" % (index,))
        if index.step is not None:
            raise IndexError("Stepped slices not yet supported: %r"
                             % (index.step,))

        offset = self._offset
        limit = self._limit

        if index.start is not None:
            if offset is Undef:
                offset = index.start
            else:
                offset += index.start
            if limit is not Undef:
                limit = max(0, limit - index.start)

        if index.stop is not None:
            if index.start is None:
                new_limit = index.stop
            else:
                new_limit = index.stop - index.start
            if limit is Undef or limit > new_limit:
                limit = new_limit

        return self.copy().config(offset=offset, limit=limit)

    def __contains__(self, item):
        """Check if an item is contained within the result set."""
        columns, values = self._find_spec.get_columns_and_values_for_item(item)

        if self._select is Undef and self._group_by is Undef:
            # No predefined select: adjust the where clause.
            dummy, default_tables = self._find_spec.get_columns_and_tables()
            where = [Eq(*pair) for pair in zip(columns, values)]
            if self._where is not Undef:
                where.append(self._where)
            select = Select(1, And(*where), self._tables,
                            default_tables)
        else:
            # Rewrite the predefined query and use it as a subquery.
            aliased_columns = [Alias(column, "_key%d" % index)
                               for (index, column) in enumerate(columns)]
            subquery = replace_columns(self._get_select(), aliased_columns)
            where = [Eq(*pair) for pair in zip(aliased_columns, values)]
            select = Select(1, And(*where), Alias(subquery, "_tmp"))

        result = self._store._connection.execute(select)
        return result.get_one() is not None

    def is_empty(self):
        """Return true if this L{ResultSet} contains no results."""
        subselect = self._get_select()
        subselect.limit = 1
        select = Select(1, tables=Alias(subselect, "_tmp"), limit=1)
        result = self._store._connection.execute(select)
        return (not result.get_one())

    def any(self):
        """Return a single item from the result set.

        See also one(), first(), and last().
        """
        select = self._get_select()
        select.limit = 1
        result = self._store._connection.execute(select)
        values = result.get_one()
        if values:
            return self._load_objects(result, values)
        return None

    def first(self):
        """Return the first item from an ordered result set.

        Will raise UnorderedError if the result set isn't ordered.

        See also last(), one(), and any().
        """
        if self._order_by is Undef:
            raise UnorderedError("Can't use first() on unordered result set")
        return self.any()

    def last(self):
        """Return the last item from an ordered result set.

        Will raise UnorderedError if the result set isn't ordered.

        See also first(), one(), and any().
        """
        if self._order_by is Undef:
            raise UnorderedError("Can't use last() on unordered result set")
        if self._limit is not Undef:
            raise FeatureError("Can't use last() with a slice "
                               "of defined stop index")
        select = self._get_select()
        select.offset = Undef
        select.limit = 1
        select.order_by = []
        for expr in self._order_by:
            if isinstance(expr, Desc):
                select.order_by.append(expr.expr)
            elif isinstance(expr, Asc):
                select.order_by.append(Desc(expr.expr))
            else:
                select.order_by.append(Desc(expr))
        result = self._store._connection.execute(select)
        values = result.get_one()
        if values:
            return self._load_objects(result, values)
        return None

    def one(self):
        """Return one item from a result set containing at most one item.

        Will raise NotOneError if the result set contains more than one item.

        See also first(), one(), and any().
        """
        select = self._get_select()
        # limit could be 1 due to slicing, for instance.
        if select.limit is not Undef and select.limit > 2:
            select.limit = 2
        result = self._store._connection.execute(select)
        values = result.get_one()
        if result.get_one():
            raise NotOneError("one() used with more than one result available")
        if values:
            return self._load_objects(result, values)
        return None

    def order_by(self, *args):
        """Specify the ordering of the results.

        The query will be modified appropriately with an ORDER BY clause.

        Ascending and descending order can be specified by wrapping
        the columns in L{Asc} and L{Desc}.

        @param args: One or more L{vnf.components.expr.Column} objects.
        """
        if self._offset is not Undef or self._limit is not Undef:
            raise FeatureError("Can't reorder a sliced result set")
        self._order_by = args or Undef
        return self

    def remove(self):
        """Remove all rows represented by this ResultSet from the database.

        This is done efficiently with a DELETE statement, so objects
        are not actually loaded into Python.
        """
        if self._group_by is not Undef:
            raise FeatureError("Removing isn't supported after a "
                               " GROUP BY clause ")
        if self._offset is not Undef or self._limit is not Undef:
            raise FeatureError("Can't remove a sliced result set")
        if self._find_spec.default_cls_info is None:
            raise FeatureError("Removing not yet supported for tuple or "
                               "expression finds")
        if self._select is not Undef:
            raise FeatureError("Removing isn't supported with "
                               "set expressions (unions, etc)")
        self._store._connection.execute(
            Delete(self._where, self._find_spec.default_cls_info.table),
            noresult=True)

    def group_by(self, *expr):
        """Group this ResultSet by the given expressions.

        @param expr: The expressions used in the GROUP BY statement.

        @return: self (not a copy).
        """
        if self._select is not Undef:
            raise FeatureError("Grouping isn't supported with "
                               "set expressions (unions, etc)")

        find_spec = FindSpec(expr)
        columns, dummy = find_spec.get_columns_and_tables()

        self._group_by = columns
        return self

    def having(self, *expr):
        """Filter result previously grouped by.

        @param expr: Instances of L{Expr}.

        @return: self (not a copy).
        """
        if self._group_by is Undef:
            raise FeatureError("having can only be called after group_by.")
        self._having = And(*expr)
        return self

    def _aggregate(self, expr, column=None):
        if self._group_by is not Undef:
            raise FeatureError("Single aggregates aren't supported after a "
                               " GROUP BY clause ")
        dummy, default_tables = self._find_spec.get_columns_and_tables()
        if self._select is Undef:
            select = Select(expr, self._where, self._tables, default_tables)
        else:
            select = Select(expr, tables=Alias(self._select))
        result = self._store._connection.execute(select)
        value = result.get_one()[0]
        variable_factory = getattr(column, "variable_factory", None)
        if variable_factory:
            variable = variable_factory()
            result.set_variable(variable, value)
            return variable.get()
        return value

    def count(self, expr=Undef, distinct=False):
        """Get the number of objects represented by this ResultSet."""
        if (self._distinct or self._limit is not Undef or
            self._offset is not Undef):
            subselect = self._get_select()
            if expr is not Undef:
                subselect.columns = expr
            select = Select(Count(), tables=Alias(subselect, "_tmp"))
            result = self._store._connection.execute(select)
            return int(result.get_one()[0])
        else:
            return int(self._aggregate(Count(expr, distinct)))

    def max(self, expr):
        """Get the highest value from an expression."""
        return self._aggregate(Max(expr), expr)

    def min(self, expr):
        """Get the lowest value from an expression."""
        return self._aggregate(Min(expr), expr)

    def avg(self, expr):
        """Get the average value from an expression."""
        value = self._aggregate(Avg(expr))
        if value is None:
            return value
        return float(value)

    def sum(self, expr):
        """Get the sum of all values in an expression."""
        return self._aggregate(Sum(expr), expr)

    def values(self, *columns):
        """Retrieve only the specified columns.

        This does not load full objects from the database into Python.

        @param columns: One or more L{vnf.components.expr.Column} objects whose
            values will be fetched.
        @return: An iterator of tuples of the values for each column
            from each matching row in the database.
        """
        if not columns:
            raise FeatureError("values() takes at least one column "
                               "as argument")
        select = self._get_select()
        select.columns = columns
        result = self._store._connection.execute(select)
        if len(columns) == 1:
            variable = columns[0].variable_factory()
            for values in result:
                result.set_variable(variable, values[0])
                yield variable.get()
        else:
            variables = [column.variable_factory() for column in columns]
            for values in result:
                for variable, value in zip(variables, values):
                    result.set_variable(variable, value)
                yield tuple(variable.get() for variable in variables)

    def set(self, *args, **kwargs):
        """Update objects in the result set with the given arguments.

        This method will update all objects in the current result set
        to match expressions given as equalities or keyword arguments.
        These objects may still be in the database (an UPDATE is issued)
        or may be cached.

        For instance, C{result.set(Class.attr1 == 1, attr2=2)} will set
        C{attr1} to 1 and C{attr2} to 2, on all matching objects.
        """
        if self._group_by is not Undef:
            raise FeatureError("Setting isn't supported after a "
                               " GROUP BY clause ")

        if self._find_spec.default_cls_info is None:
            raise FeatureError("Setting isn't supported with tuple or "
                               "expression finds")
        if self._select is not Undef:
            raise FeatureError("Setting isn't supported with "
                               "set expressions (unions, etc)")

        if not (args or kwargs):
            return

        changes = {}
        cls = self._find_spec.default_cls_info.cls

        # For now only "Class.attr == var" is supported in args.
        for expr in args:
            if (not isinstance(expr, Eq) or
                not isinstance(expr.expr1, Column) or
                not isinstance(expr.expr2, (Column, Variable))):
                raise FeatureError("Unsupported set expression: %r" %
                                   repr(expr))
            changes[expr.expr1] = expr.expr2

        for key, value in kwargs.items():
            column = getattr(cls, key)
            if value is None:
                changes[column] = None
            elif isinstance(value, Expr):
                if not isinstance(value, Column):
                    raise FeatureError("Unsupported set expression: %r" %
                                       repr(value))
                changes[column] = value
            else:
                changes[column] = column.variable_factory(value=value)

        expr = Update(changes, self._where,
                      self._find_spec.default_cls_info.table)
        self._store.execute(expr, noresult=True)

        try:
            cached = self.cached()
        except CompileError:
            for obj_info in self._store._iter_alive():
                for column in changes:
                    obj_info.variables[column].set(AutoReload)
        else:
            changes = changes.items()
            for obj in cached:
                for column, value in changes:
                    variables = get_obj_info(obj).variables
                    if value is None:
                        pass
                    elif isinstance(value, Variable):
                        value = value.get()
                    else:
                        value = variables[value].get()
                    variables[column].set(value)
                    variables[column].checkpoint()

    def cached(self):
        """Return matching objects from the cache for the current query."""
        if self._find_spec.default_cls_info is None:
            raise FeatureError("Cache finds not supported with tuples "
                               "or expressions")
        if self._tables is not Undef:
            raise FeatureError("Cache finds not supported with custom tables")
        if self._where is Undef:
            match = None
        else:
            match = compile_python.get_matcher(self._where)
            name_to_column = dict(
                (column.name, column)
                for column in self._find_spec.default_cls_info.columns)
            def get_column(name, name_to_column=name_to_column):
                return obj_info.variables[name_to_column[name]].get()
        objects = []
        cls = self._find_spec.default_cls_info.cls
        for obj_info in self._store._iter_alive():
            try:
                if (obj_info.cls_info is self._find_spec.default_cls_info and
                    (match is None or match(get_column))):
                    objects.append(self._store._get_object(obj_info))
            except LostObjectError:
                pass # This may happen when resolving lazy values
                     # in get_column().
        return objects

    def _set_expr(self, expr_cls, other, all=False):
        if not self._find_spec.is_compatible(other._find_spec):
            raise FeatureError("Incompatible results for set operation")

        expr = expr_cls(self._get_select(), other._get_select(), all=all)
        return ResultSet(self._store, self._find_spec, select=expr)

    def union(self, other, all=False):
        """Get the L{Union} of this result set and another.

        @param all: If True, include duplicates.
        """
        if isinstance(other, EmptyResultSet):
            return self
        return self._set_expr(Union, other, all)

    def difference(self, other, all=False):
        """Get the difference, using L{Except}, of this result set and another.

        @param all: If True, include duplicates.
        """
        if isinstance(other, EmptyResultSet):
            return self
        return self._set_expr(Except, other, all)

    def intersection(self, other, all=False):
        """Get the L{Intersection} of this result set and another.

        @param all: If True, include duplicates.
        """
        if isinstance(other, EmptyResultSet):
            return other
        return self._set_expr(Intersect, other, all)


class EmptyResultSet(object):
    """An object that looks like a L{ResultSet} but represents no rows.

    This is convenient for application developers who want to provide
    a method which is guaranteed to return a L{ResultSet}-like object
    but which, in certain cases, knows there is no point in querying
    the database. For example::

        def get_people(self, ids):
            if not ids:
                return EmptyResultSet()
            return store.find(People, People.id.is_in(ids))

    The methods on EmptyResultSet (L{one}, L{config}, L{union}, etc)
    are meant to emulate a L{ResultSet} which has matched no rows.
    """

    def __init__(self, ordered=False):
        self._order_by = ordered

    def _get_select(self):
        return Select(SQLRaw("1"), SQLRaw("1 = 2"))

    def copy(self):
        result = EmptyResultSet(self._order_by)
        return result

    def config(self, distinct=None, offset=None, limit=None):
        pass

    def __iter__(self):
        return
        yield None

    def __getitem__(self, index):
        return self.copy()

    def __contains__(self, item):
        return False

    def is_empty(self):
        return True

    def any(self):
        return None

    def first(self):
        if self._order_by:
            return None
        raise UnorderedError("Can't use first() on unordered result set")

    def last(self):
        if self._order_by:
            return None
        raise UnorderedError("Can't use last() on unordered result set")

    def one(self):
        return None

    def order_by(self, *args):
        self._order_by = True
        return self

    def remove(self):
        pass

    def count(self, expr=Undef, distinct=False):
        return 0

    def max(self, column):
        return None

    def min(self, column):
        return None

    def avg(self, column):
        return None

    def sum(self, column):
        return None

    def values(self, *columns):
        if not columns:
            raise FeatureError("values() takes at least one column "
                               "as argument")
        return
        yield None

    def set(self, *args, **kwargs):
        pass

    def cached(self):
        return []

    def union(self, other):
        if isinstance(other, EmptyResultSet):
            return self
        return other.union(self)

    def difference(self, other):
        return self

    def intersection(self, other):
        return self


class TableSet(object):
    """The representation of a set of tables which can be queried at once.

    This will typically be constructed by a call to L{Store.using}.
    """

    def __init__(self, store, tables):
        self._store = store
        self._tables = tables

    def find(self, cls_spec, *args, **kwargs):
        """Perform a query on the previously specified tables.

        This is identical to L{Store.find} except that the tables are
        explicitly specified instead of relying on inference.

        @return: A L{ResultSet}.
        """
        if self._store._implicit_flush_block_count == 0:
            self._store.flush()
        find_spec = FindSpec(cls_spec)
        where = get_where_for_args(args, kwargs, find_spec.default_cls)
        return self._store._result_set_factory(self._store, find_spec,
                                               where, self._tables)

    
Clerk._result_set_factory = ResultSet
Clerk._table_set = TableSet

class FindSpec(object):
    """The set of tables or expressions in the result of L{Store.find}."""

    def __init__(self, cls_spec):
        self.is_tuple = type(cls_spec) == tuple
        if not self.is_tuple:
            cls_spec = (cls_spec,)

        info = []
        for item in cls_spec:
            if isinstance(item, Expr):
                info.append((True, item))
            else:
                info.append((False, get_cls_info(item)))
        self._cls_spec_info = tuple(info)

        # Do we have a single non-expression item here?
        if not self.is_tuple and not info[0][0]:
            self.default_cls = cls_spec[0]
            self.default_cls_info = info[0][1]
            self.default_order = self.default_cls_info.default_order
        else:
            self.default_cls = None
            self.default_cls_info = None
            self.default_order = Undef

    def get_columns_and_tables(self):
        columns = []
        default_tables = []
        for is_expr, info in self._cls_spec_info:
            if is_expr:
                columns.append(info)
                if isinstance(info, Column):
                    default_tables.append(info.table)
            else:
                columns.extend(info.columns)
                default_tables.append(info.table)
        return columns, default_tables

    def is_compatible(self, find_spec):
        """Return True if this FindSpec is compatible with a second one."""
        if self.is_tuple != find_spec.is_tuple:
            return False
        if len(self._cls_spec_info) != len(find_spec._cls_spec_info):
            return False
        for (is_expr1, info1), (is_expr2, info2) in zip(
            self._cls_spec_info, find_spec._cls_spec_info):
            if is_expr1 != is_expr2:
                return False
            if info1 is not info2:
                return False
        return True

    def load_objects(self, store, result, values):
        objects = []
        values_start = values_end = 0
        for is_expr, info in self._cls_spec_info:
            if is_expr:
                values_end += 1
                variable = getattr(info, "variable_factory", Variable)(
                    value=values[values_start], from_db=True)
                objects.append(variable.get())
            else:
                values_end += len(info.columns)
                obj = store._load_object(info, result,
                                         values[values_start:values_end])
                objects.append(obj)
            values_start = values_end
        if self.is_tuple:
            return tuple(objects)
        else:
            return objects[0]

    def get_columns_and_values_for_item(self, item):
        """Generate a comparison expression with the given item."""
        if isinstance(item, tuple):
            if not self.is_tuple:
                raise TypeError("Find spec does not expect tuples.")
        else:
            if self.is_tuple:
                raise TypeError("Find spec expects tuples.")
            item = (item,)

        columns = []
        values = []
        for (is_expr, info), value in zip(self._cls_spec_info, item):
            if is_expr:
                if not isinstance(value, (Expr, Variable)) and (
                    value is not None):
                    value = getattr(info, "variable_factory", Variable)(
                        value=value)
                columns.append(info)
                values.append(value)
            else:
                obj_info = get_obj_info(value)
                if obj_info.cls_info != info:
                    raise TypeError("%r does not match %r" % (value, info))
                columns.extend(info.primary_key)
                values.extend(obj_info.primary_vars)
        return columns, values


def get_where_for_args(args, kwargs, cls=None):
    equals = list(args)
    if kwargs:
        if cls is None:
            raise Exception("Can't determine class that keyword "
                               "arguments are associated with")
        for key, value in kwargs.items():
            equals.append(getattr(cls, key) == value)
    if equals:
        return And(*equals)
    return Undef

def replace_columns(expr, columns):
    if isinstance(expr, Select):
        select = copy(expr)
        select.columns = columns
        # Remove the ordering if it won't affect the result of the query.
        if select.limit is Undef and select.offset is Undef:
            select.order_by = Undef
        return select
    elif isinstance(expr, SetExpr):
        # The ORDER BY clause might refer to columns we have replaced.
        # Luckily we can ignore it if there is no limit/offset.
        if expr.order_by is not Undef and (
            expr.limit is not Undef or expr.offset is not Undef):
            raise FeatureError(
                "__contains__() does not yet support set "
                "expressions that combine ORDER BY with "
                "LIMIT/OFFSET")
        subexprs = [replace_columns(subexpr, columns)
                    for subexpr in expr.exprs]
        return expr.__class__(
            all=expr.all, limit=expr.limit, offset=expr.offset,
            *subexprs)
    else:
        raise FeatureError(
            "__contains__() does not yet support %r expressions"
            % (expr.__class__,))
        
class AutoReload(LazyValue):
    """A marker for reloading a single value.

    Often this will be used to specify that a specific attribute
    should be loaded from the database on the next access, like so::

        vnf_object.property = AutoReload

    On the next access to C{vnf_object.property}, the value will be
    loaded from the database.

    It is also often used as a default value for a property::

        class Person(object):
            __storm_table__ = "person"
            id = Int(allow_none=False, default=AutoReload)

        person = store.add(Person)
        person.id # gets the attribute from the database.
    """
    pass

AutoReload = AutoReload()

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
