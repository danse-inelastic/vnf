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

    def checkPrivilege(self, user, privilege):
        db = self.db
        return acl.checkPrivilege(user, privilege, db)
    

import vnf.dom.acl as acl

# version
__id__ = "$Id$"

# End of file 
