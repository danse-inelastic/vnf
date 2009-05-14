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


    # temp hack to limit access to vasp
    def checkVASPPrivilege(self, user):
        caltechgroup = [
            'altafang',
            'btf',
            'chen',
            'dabrecht',
            'dexity',
            'jbrkeith',
            'linjiao',
            'markovsk',
            'mmckerns',
            'aivazis',
            'olivier',
            'winterro',
            ]
        whitelist = caltechgroup
        return user.username in whitelist
    

    def _checkPrivilege(self, user, privilege):
        db = self.db
        return acl.checkPrivilege(user, privilege, db)
    

import vnf.dom.acl as acl

# version
__id__ = "$Id$"

# End of file 
