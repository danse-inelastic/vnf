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


# copied from vnf-alpha. need a lot of rework


class AccessControl:

    # data member needed
    sentry = None
    clerk = None


    def checkPrivilege(self, target, name, username=None):
        if not username:
            username = self.sentry.username
        clerk = self.clerk
        user = clerk.getUser(username)
        db = clerk.db
        privilege = target,name
        return user.hasPrivilege(privilege, db)
    

    # this is obsolete. should use the new acl tables
    def checkInstrumentPrivilege(self, user, instrument):
        # if instrument is owned by user, fine
        if instrument.creator == user.username:
            return True
        # if instrument is owned by users other than "vnf", no
        if instrument.creator != 'vnf':
            return False
        # for now allow anyone to access any instruments
        return True


    # this is obsolete. should use the new acl tables
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
            'lmauger',
            'markovsk',
            'mmckerns',
            'aivazis',
            'olivier',
            'purewal',
            'winterro',
            ]
        whitelist = caltechgroup
        return user.username in whitelist
    


# version
__id__ = "$Id$"

# End of file 
