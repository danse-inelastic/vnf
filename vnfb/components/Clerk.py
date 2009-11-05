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


class Clerk( base ):

    class Inventory( base.Inventory):

        import pyre.inventory
        db = pyre.inventory.str('db', default = 'vnf' )
        

    def __init__(self, name = 'clerk', facility = 'clerk'):
        base.__init__(self, name, facility=facility)
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
        

    def _configure(self):
        base._configure(self)
        self.db = self.inventory.db
        return


    def _init(self):
        base._init(self)

        from dsaw.db import connect
        self.db = connect(db=self.db)
        self.db.autocommit(True)

        # create system tables if necessary
##         system_tables = self.db._systemtables
##         for table in system_tables.itertables():
##             try:
##                 self.db.createTable(table)
##             except:
##                 import traceback
##                 traceback.print_exc()
##             continue

        # register tables
        from vnf.dom import alltables
        for table in alltables():
            self.db.registerTable(table)
        return


    def _fini(self):
        base._fini(self)
        return
    


# version
__id__ = "$Id$"

# End of file 
