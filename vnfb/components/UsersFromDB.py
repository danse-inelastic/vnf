# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.ipa.UserManager import UserManager as base
from pyre.components.Component import Component

class UsersFromDB(base):
    
    class Inventory(Component.Inventory):

        import pyre.inventory

        import vnfb.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnfb.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"
        pass # end of Inventory


    def load(self):
        clerk = self.clerk
        try:
            method = clerk.getUser('__method__').password
        except:
            raise RuntimeError, "A fake user '__method__' must exists and its 'password' must be the encription method"

        records = clerk.indexUsers().itervalues()
        users = {}
        for r in records:
            users[r.username] = r.password
            continue

        count = len(users)
        if count == 1:
            suffix = ''
        else:
            suffix = 's'
        self._info.log("found %d user record%s" % (count, suffix))

        self._users = users
        self._reload = False

        self._encoder = self._encoders[method]
        self._decoder = self._decoders[method]
        return


    def save(self):
        from vnfb.dom.User import User
        for name, pw in self._users.iteritems():
            assignments = [ ('password', pw) ]
            self.clerk.db.updateRow(User, assignments, where="username='%s'" % name)
            continue
        return


    def _configure(self):
        Component._configure(self)
        self.clerk = self.inventory.clerk
        self.clerk.director = None
        return
    

    def _init(self):
        Component._init(self)
        return


# version
__id__ = "$Id$"

# End of file 
