# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2007-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.components.Component import Component as base


# domaccessor facilitates association of db with the application.
# the application must have facility to
#  1. create a unique ID
#  2. know who is the current user
#
class DOMAccessor( base ):

    director = None

    def _getOrm(self):
        return self.director.clerk.orm
    orm = property(_getOrm)


    def _getDB(self):
        return self.orm.db
    db = property(_getDB)


    def importAllDataObjects(self):
        '''in some circumstances, it is useful to know of all the data objects
        in the system. this is done by importing all modules in vnf.dom
        '''
        # actually some dom must be imported earlier than others
        from vnf.dom import AtomicStructure
        
        def _imp(m): return __import__(m, {}, {}, [''])

        #
        dompkgname = 'vnf.dom'
        dompkg = _imp(dompkgname)
        f = dompkg.__file__

        #
        import os
        directory = os.path.dirname(f)

        #
        def _importallmodules(dir, pkg):
            imported = []
            for entry in os.listdir(dir):
                # private, skip
                if entry.startswith('_'): continue
                # directory, recurse into
                # assumes that directories are all python subpackages
                p = os.path.join(dir, entry)
                if os.path.isdir(p):
                    _importallmodules(p, pkg+'.'+entry)
                    continue
                # python module
                if not entry.endswith('.py') and not entry.endswith('.pyc'): continue
                m = pkg + '.' + entry[:-3]
                if m in imported: continue
                else: imported.append(m)
                m = _imp(m)
                import inspect
                for symbol, entity in m.__dict__.iteritems():
                    if inspect.isclass(entity) \
                           and issubclass(entity, TableBase) \
                           and entity is not TableBase \
                           and entity.tablenameIsDefined():
                        self.db.registerTable(entity)
                continue
            return

        _importallmodules(directory, dompkgname)
        return


    def __init__(self, name, facility = 'dom-accessor'):
        super(DOMAccessor, self).__init__(name, facility)
        return


    # initialization methods
    def setApplicationDirector(self, director):
        self.director = director
        return


    def setDB(self, db):
        self.db = db
        return


    def set(self, db=None, director=None):
        if db: self.setDB(db)
        if director: self.setApplicationDirector(director)
        return


    # transient objects
    def isTransient(self, record):
        gp = record.globalpointer
        if not gp: return False
        from vnf.dom.TransientObject import TransientObject
        q = self.db.query(TransientObject).filter_by(
            target = record.globalpointer.id)
        r = q.all()
        return bool(len(r))


    def setTransient(self, record):
        from vnf.dom.TransientObject import TransientObject
        row = TransientObject()
        row.target = record
        self.db.insertRow(row)
        return


    def removeTransient(self, record):
        from vnf.dom.TransientObject import TransientObject
        q = self.db.query(TransientObject).filter_by(
            target = record.globalpointer.id)
        rs = q.all()
        if len(rs)==0: return
        for r in rs:
            self.db.deleteRow(TransientObject, where="id='%s'" % r.id)
            continue
        return
    
        
    # access to proxy
    def makeProxy(self, record, factory):
        return factory(record, domaccess=self)
    
    
    # generic accessing methods
    def updateRecordWithID(self, record):
        'update a record. assumes that it has a "id" column'
        return self.db.updateRecord(record)


    def getRecordByID(self, tablename, id):
        if isinstance(tablename, basestring):
            Table = self._getTable(tablename)
        elif issubclass(tablename, TableBase):
            Table = tablename
        else:
            raise ValueError, 'tablename must be a string or a table class: %s' % tablename
        return self._getRecordByID(Table, id)
    
    
    def insertNewOwnedRecord(self, table, owner = None):
        '''create a new record for the given table.

        The given table is assumed to have following fields:
          - id
          - creator
          - date
        '''
        if isinstance(table, str): table = self._getTable(table)
        
        director = self.director
        id = director.getGUID()

        record = table()
        record.id = id

        if not owner: 
            owner = director.sentry.username
        record.creator = owner
        
        self.insertNewRecord( record )
        return record


    def insertNewRecordWithID(self, table):
        '''create a new record for the given table and store it in the db.

        The given table is assumed to have following fields:
          - id
        '''
        record = self.createRecordWithID(table)
        return self.insertNewRecord(record)
    
    
    def createRecordWithID(self, table):
        '''create a new record for the given table but do not store it in the db.

        The given table is assumed to have following fields:
          - id
        '''
        record = table()
        
        director = self.director
        id = director.getGUID()
        record.id = id

        return record


    def insertNewRecord(self, record):
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


    def deleteRecordWithID(self, record):
        'delete a record. assumes that it has a "id" column'
        self.db.deleteRow(record.__class__, where="id='%s'" % record.id)
        return
    

    def dereference(self, pointer):
        '''dereference a "pointer"'''
        return pointer.dereference(self.db)


    def findDuplicateRecord(self, obj):
        """
        EXPERIMENTAL!!!
        
        find a record that has the same signature as the given object
        
        assumption:
        * The class of the object has a property "key_props" that is 
          a list of names of key properties of the object 
          
        """
        orm = self.orm
        record = orm(obj)
        Object = obj.__class__
        Table = record.__class__
        #
        kwds = {}
        for key in Object.key_props:
            value = getattr(record, key)
            descriptor = Object.Inventory.getDescriptor(key)
            # for reference types, id is the signature
            if descriptor.type.find('reference') != -1:
                if value is not None:
                    value = value.id
            kwds[key] = value
            continue
        records = self.db.query(Table).filter_by(**kwds).all()
        if len(records)>1:
            for r in records:
                if r.id != record.id:
                    return r
        return

    #
    def _getUsername(self):
        return self.director.sentry.username


    def _getTable(self, name):
        '''return the table given a specifier of the table
        
        If the table is already registered with db manager,
        you can specify the table by its name. E.g.

          >>> class A(Table):
            name = 'a'
            ...
          >>> domaccess.db.registerTable(A)
          >>> domaccess._getTable('a')  # return A

        If the table is not yet registered, you can specify 
        it by its place in vnf.dom namespace. 

        For example, there is a class ATable which is a table and
        is defined in vnf.dom.subpkg.A module. Then

          >>> domaccess._getTable('subpkg.A.ATable')

        You could also just specify the place of a data object
        instead of a table. Suppose class A is the class of a
        data object (not a table), and is defined in 
        vnf.dom.subpkg.A module, then

          >>> domaccess._getTable('subpkg.A.A')
        '''
        try:
            return self.db.getTable(name)
        except:
            import traceback
            self._debug.log(traceback.format_exc())
            return self._getTableByImportingFromDOM(name)


    def _getObjectByImportingFromDOM(self, name):
        pkg = 'vnf.dom'
        domains = name.split('.')
        module = '%s.%s' % (pkg, '.'.join(domains[:-1]))
        try:
            exec 'from %s import %s as Obj' % (module, domains[-1])
        except ImportError:
            import traceback
            error = traceback.format_exc()
            raise RuntimeError, 'failed to resolve data object type %s by importing.\n%s' % (
                name, error)
        return Obj


    def _getTableByImportingFromDOM(self, name):
        table = self._getObjectByImportingFromDOM(name)
        if not issubclass(table, TableBase):
            orm = self.orm
            Obj = table
            table = orm(Obj)
        else:
            self.db.registerTable(table)
        return table


    def _getRecordByID(self, table, id ):
        all = self.db.fetchall( table, where = "id='%s'" % id )
        if len(all) == 1:
            return all[0]
        raise RuntimeError, "Cannot find record of id=%s in table %s" % (
            id, table.__name__)

    def _getAll(self, table, where = None):
        #index = {}
        all = self.db.fetchall(table, where=where)
        return all

    
    """Auxiliary classes"""
    
    def _getClass(self, classname, maindom = "vnf.dom"):
        """Get class from classname"""
        module  = _import("%s.%s" % (maindom, classname))
        return getattr(module, classname)


    def _getEntry(self, classname, id=None, where=None, maindom="vnf.dom"):
        """Get entry specified by id or where clause"""
        table = self._getClass(classname, maindom)
        if id is not None:
            return self._getRecordByID( table, id )

        return self._getAll(table, where)




from dsaw.db.Table import Table as TableBase



class Proxy(object):

    
    def __init__(self, record, domaccess=None):
        self.record = record
        self.domaccess = domaccess
        self.db = domaccess.db
        return


    def __getattr__(self, name):
        o = self._getObject()
        if hasattr(o, name): return getattr(o, name)
        return getattr(self.record, name)


    def _getObject(self):
        if not '_object' in self.__dict__:
            try:
                o = self._convertToObject()
            except:
                import traceback
                raise RuntimeError, 'failed to convert record %s:%s to object: %s' % (
                    self.record.__class__.getTableName(), self.record.id, traceback.format_exc())
            
            setattr(self, '_object', o)
        return self._object


    def _setObjectObsolete(self):
        if self.__dict__.has_key('_object'):
            del self.__dict__['_object']


    def _convertToObject(self):
        raise NotImplementedError


def _import(package):
    return __import__(package, {}, {}, [''])


# version
__id__ = "$Id$"

#    # Added from old Clerk, same as updateRecordWithID()?
#    def updateRecord(self, record):
#        """Updates row in the database specified by record.id"""
#        id = record.id
#        where = "id='%s'" % id
#
#        assignments = []
#
#        # get the column names and couple them with the new values
#        for column in record.getColumnNames():
#            value = getattr( record, column )
#            assignments.append( (column, value) )
#            continue
#        # update the row, or in other words, record
#        self.db.updateRow(record.__class__, assignments, where)
#        return record



# End of file 
