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


from DOMAccessor import DOMAccessor as base
from luban.components.Clerk import Clerk as ClerkBase

class Clerk(base, ClerkBase):

    class Inventory(ClerkBase.Inventory, base.Inventory):

        import pyre.inventory
        db = pyre.inventory.str('db', default = 'vnf' )
        echo = pyre.inventory.bool('echo', default=False)
        

    def __init__(self, name = 'clerk', facility = 'clerk'):
        ClerkBase.__init__(self, name, facility=facility)
        return
    

    # user table
    def indexUsers(self, where=None):
        """create an index of all users that meet the specified criteria"""
        from vnfb.dom.User import User
        index = {}
        users = self.db.fetchall(User, where=where)
        for user in users:
            index[user.username] = user
            continue
        return index


    def indexActiveUsers(self):
        return self.indexUsers()


    def getUser(self, username):
        from vnfb.dom.User import User
        users = self.db.fetchall(User, where="username='%s'" % username)
        if not users: raise RuntimeError, "user %r not found" % username
        assert len(users) == 1
        return users[0]


    def getUserInfo(self, username):
        from vnfb.dom.Registrant import Registrant
        registrants = self.db.fetchall(Registrant, where="username='%s'"% username)
        if not registrants: raise RuntimeError, "user %r not found" % username
        assert len(registrants) == 1
        return registrants[0]
        

    """QE methods for retrieving records using vnfb.dom"""

    def getQEJobs(self, id=None, where=None):
        '''retrieve qejobs record specified by id'''
        return self._getEntry('QEJob', id=id, where=where)

    def getQESimulations(self, id=None, where=None):
        '''retrieve simulation record specified by id'''
        return self._getEntry('QESimulation', id=id, where=where)

    def getQESimulationTasks(self, id=None, where=None):
        '''retrieve simulation task record specified by id'''
        return self._getEntry('QESimulationTask', id=id, where=where)

    def getQEConfigurations(self, id=None, where=None):
        '''retrieve user configuration specified by id'''
        return self._getEntry('QEConfiguration', id=id, where=where)

    def getQESettings(self, id=None, where=None):
        '''retrieve simulation settings specified by id'''
        return self._getEntry('QESetting', id=id, where=where)

    def getQETasks(self, id=None, where=None):
        '''retrieve task specified by id'''
        return self._getEntry('QETask', id=id, where=where)

    def getQEConvergences(self, id=None, where=None):
        '''retrieve convergence tests specified by id'''
        return self._getEntry('QEConvergence', id=id, where=where)

    def getQEConvParams(self, id=None, where=None):
        '''retrieve convergence parameters specified by id'''
        return self._getEntry('QEConvParam', id=id, where=where)

    def getQEConvParamTasks(self, id=None, where=None):
        '''retrieve convergence tasks specified by id'''
        return self._getEntry('QEConvParamTask', id=id, where=where)



    # Temp solution
    def getServers(self, id=None, where=None):
        '''retrieve server data specified by id'''
        return self._getEntry('Server', id=id, where=where)



    # register tables that are not in orm
    def _registerTables(self, db):
        from vnfb.dom import tables_without_orm
        for table in tables_without_orm():
            db.registerTable(table)
        return


    # orm
    def _getOrm(self):
        if not hasattr(self, '_orm'):
            self._createOrmManager()
        return self._orm
    orm = property(_getOrm)
    

    def _createOrmManager(self):
        director = self.director
        guid = director.getGUID
        db = self.db
        from vnfb.dom import object2table
        from dsaw.model.visitors.OrmManager import OrmManager
        self._orm = OrmManager(db=db, guid=guid, object2table=object2table)
        return
        

    def _getDB(self):
        if not hasattr(self, '_db'):
            self._db = self._createDB()
        return self._db
    db = property(_getDB)
    
    
    def _createDB(self):
        db = self.inventory.db
        from dsaw.db import connect
        db = connect(db=db, echo=self.inventory.echo)
        self._registerTables(db)
        return db



# version
__id__ = "$Id$"

# End of file 
