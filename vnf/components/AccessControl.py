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
        # check special privilege
        any = instrument.__class__()
        any.id = 'any'
        if self._checkPrivilege(user, any): return True
        return self._checkPrivilege(user, instrument)
    

    def _checkPrivilege(self, user, privilege):
        db = self.db
        return acl.checkPrivilege(user, privilege, db)
    

import vnf.dom.acl as acl

# version
__id__ = "$Id$"

# End of file 
