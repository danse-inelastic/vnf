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



class AccessControl:

    # data member needed
    db = None


    def checkInstrumentPrivilege(self, user, instrument):
        # if instrument is owned by user, fine
        if instrument.creator == user.username:
            return True
        # if instrument is owned by users other than "vnf", no
        if instrument.creator != 'vnf':
            return False
        # for now allow anyone to access any instruments
        return True
    

    def _checkPrivilege(self, user, privilege):
        db = self.db
        return acl.checkPrivilege(user, privilege, db)
    

import vnf.dom.acl as acl

# version
__id__ = "$Id$"

# End of file 
