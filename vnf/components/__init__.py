# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def dds():
    from DistributedDataStorage import DistributedDataStorage
    return DistributedDataStorage('dds', 'dds')


def clerk():
    from Clerk import Clerk
    return Clerk('clerk', 'clerk')


def ssher(name='ssher', facility='csaccessor'):
    from SSHer import SSHer
    return SSHer(name=name, facility=facility)


def usersFromDB():
    from UsersFromDB import UsersFromDB
    return UsersFromDB('usersFromDB')


def accesscontrol():
    from AccessControl import AccessControl
    return AccessControl()


# communications
def announcer():
    from Announcer import Announcer
    return Announcer()


def postman():
    from Postman import Postman
    return Postman()


# version
__id__ = "$Id$"

# End of file 
