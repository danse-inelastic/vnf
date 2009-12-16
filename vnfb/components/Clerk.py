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


class Clerk(ClerkBase, base):

    class Inventory(ClerkBase.Inventory, base.Inventory):

        import pyre.inventory
        db = pyre.inventory.str('db', default = 'vnf' )
        

    def __init__(self, name = 'clerk', facility = 'clerk'):
        ClerkBase.__init__(self, name, facility=facility)
        return
    

    # user table
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
        return self.indexUsers()


    def getUser(self, username):
        from vnf.dom.User import User
        users = self.db.fetchall(User, where="username='%s'" % username)
        if not users: raise RuntimeError, "user %r not found" % username
        assert len(users) == 1
        return users[0]


    def getUserInfo(self, username):
        from vnf.dom.Registrant import Registrant
        registrants = self.db.fetchall(Registrant, where="username='%s'"% username)
        if not registrants: raise RuntimeError, "user %r not found" % username
        assert len(registrants) == 1
        return registrants[0]
        

    """QE methods for retrieving records using vnf.dom"""

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

    # Temp solution
    def getServers(self, id=None, where=None):
        '''retrieve server data specified by id'''
        return self._getEntry('Server', id=id, where=where)



    # for compatibility with vnf-alpha. should eventually remove
    def _registerVnfAlphaTables(self, db):
        # register tables
        from vnf.dom import alltables
        for table in alltables():
            db.registerTable(table)
        return


    def _createOrmManager(self):
        director = self.director
        guid = director.getGUID
        db = self.db
        from vnfb.dom import object2table
        from dsaw.model.visitors.OrmManager import OrmManager
        self._orm = OrmManager(db=db, guid=guid, object2table=object2table)
        return
        
    
    def _createDB(self):
        db = self.inventory.db
        from dsaw.db import connect
        db = connect(db=db)
        self._registerVnfAlphaTables(db)
        return db



# version
__id__ = "$Id$"

# End of file 
