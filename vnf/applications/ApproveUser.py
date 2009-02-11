#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2008  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.applications.Script import Script as base

class ApproveUser(base):

    class Inventory(base.Inventory):

        import pyre.inventory
        username = pyre.inventory.str('username')

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnf.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        debug = pyre.inventory.bool(name='debug', default=False)
        pass # end of Inventory
        

    def main(self):
        username = self.username
        from vnf.dom.Registrant import Registrant
        where = "username='%s'" % username
        registrant = self.clerk.db.fetchall(Registrant, where=where)[0]

        from vnf.dom.User import User
        user = User()
        user.username = user.id = username
        user.password = registrant.password
        user.fullname = '%s %s' % (registrant.firstname, registrant.lastname)
        user.email = registrant.email
        
        self.clerk.newRecord(user)

        from vnf.components.misc import announce
        # send an acknowlegement to user
        announce(self, 'user-approval', user)
        # alert administrators
        announce(self, 'user-approval-alert', user)
        return


    def __init__(self, name='submitjob'):
        base.__init__(self, name)
        return


    def _configure(self):
        base._configure(self)
        self.username = self.inventory.username

        self.debug = self.inventory.debug

        self.clerk = self.inventory.clerk
        self.clerk.director = self
        return


    def _init(self):
        base._init(self)

        # initialize table registry
        import vnf.dom
        vnf.dom.register_alltables()

        # set id generator for referenceset
        def _id():
            from vnf.components.misc import new_id
            return new_id(self)
        vnf.dom.set_idgenerator(_id)
        return



# version
__id__ = "$Id$"

# End of file 
