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


from luban.applications.UIApp import UIApp as base


class ApproveUser(base):

    class Inventory(base.Inventory):

        import pyre.inventory
        username = pyre.inventory.str('username')
        debug = pyre.inventory.bool(name='debug', default=False)
        pass # end of Inventory
        

    def main(self):
        username = self.username
        if username:
            self.approve(username)

        from vnfb.utils.services.ipad import askIpadToReload
        askIpadToReload(self)
        return


    def approve(self, username):
        from vnfb.dom.Registrant import Registrant
        where = "username='%s'" % username
        registrant = self.clerk.db.query(Registrant).filter_by(username=username).one()

        from vnfb.dom.User import User
        user = User()
        user.username = user.id = username
        user.password = registrant.password
        user.fullname = '%s %s' % (registrant.firstname, registrant.lastname)
        user.email = registrant.email
        
        self.clerk.db.insertRow(user)

        from vnfb.utils.communications import announce
        # send an acknowlegement to user
        announce(self, 'user-approval', user)
        # alert administrators
        # announce(self, 'user-approval-alert', user)


    def _configure(self):
        base._configure(self)
        self.username = self.inventory.username
        self.debug = self.inventory.debug
        return


    def _getPrivateDepositoryLocations(self):
        from vnfb.deployment import pyre_depositories
        return pyre_depositories



# version
__id__ = "$Id$"

# End of file 
