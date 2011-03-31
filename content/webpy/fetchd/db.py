#!/usr/bin/python
# 10/01/10
# Charles O. Goddard

import psycopg2
import time

#
# CREATE SEQUENCE fileID START 1;
# CREATE TABLE downloadedFiles (
#     id integer PRIMARY KEY DEFAULT nextval('fileID'),
#     name text UNIQUE,
#     owner text,
#     inserted timestamp,
#     original_path text,
#     data OID
# )
# 

# STILL TODO: Fix this.
connection_str = "dbname=test user=postgres password=TzjUvh"

class DBFile(object):
    '''A thin caching wrapper over a row in the database.'''
    fields = ['name', 'owner', 'inserted', 'original_path', 'data']
    def __init__(self, db, id_):
        self.__dict__["db"] = db
        self.__dict__["id"] = id_
        self.__dict__["_cache"] = {}
        
    def delete(self):
        '''Remove the corresponding entry from the database.'''
        csr = self.db.cursor()
        csr.execute("DELETE FROM downloadedFiles WHERE id=%s",(self.id,))
    
    def __getattr__(self, field):
        if not field in DBFile.fields:
            raise AttributeError("DBFile object has no attribute '%s'"%field)
        if field in self._cache:
            return self._cache[field]
        
        sqlbase = "SELECT "+field+" FROM downloadedFiles WHERE id=%s"
        csr = self.db.cursor()
        csr.execute(sqlbase, (self.id,))
        if csr.rowcount != 1:
            raise IndexError(self.id)
        ret = csr.fetchone()[0]
        self._cache[field] = ret
        return ret
    
    def __setattr__(self, field, value):
        if not field in DBFile.fields:
            raise AttributeError("DBFile object has no attribute '%s'"%field)
        if field in self._cache:
            del self._cache[field]
        
        sqlbase = "UPDATE downloadedFiles SET "+field+"=%s WHERE id=%s"
        csr = self.db.cursor()
        csr.execute(sqlbase, (value, self.id))

    def __delattr__(self, field):
        if field in self._cache:
            del self._cache[field]
    
    def data(self):
        '''
        Return a lobject instance tied to the stored OID.
        The return value can pretty much be treated as a file-like.
        '''
        return self.db.lobject(self.__getattr__('data'), 'rw')

class FileStore(object):
    def __init__(self, conn_str=connection_str):
        self.conn = psycopg2.connect(conn_str)
    
    def new(self, name, filename=None):
        blob = self.conn.lobject(0, 'w', 0, filename)
        csr = self.conn.cursor()
        csr.execute("INSERT INTO downloadedFiles (id, name, inserted, data)" +
                    "VALUES (DEFAULT, %s, %s, %s) RETURNING id",
                    (name, psycopg2.TimestampFromTicks(time.time()), blob.oid))
        id_ = csr.fetchone()[0]
        self.conn.commit()
        return DBFile(self.conn, id_)
    
    def name_exists(self, name):
        csr = self.conn.cursor()
        csr.execute("SELECT 1 FROM downloadedFiles WHERE name=%s", (name,))
        return csr.rowcount > 0
    
    def get(self, id_):
        return DBFile(self.conn, id_)
    
    def commit(self):
        self.conn.commit()
