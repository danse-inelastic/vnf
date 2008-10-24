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

def clerk():
    from Clerk import Clerk
    return Clerk( 'clerk', 'clerk' )


def scribe():
    from Scribe import Scribe
    return Scribe( 'scribe', 'scribe' )


def ssher():
    from SSHer import SSHer
    return SSHer( 'ssher', 'ssher' )


def dds():
    from DistributedDataStorage import DistributedDataStorage
    return DistributedDataStorage('dds', 'dds')


def buildjob(*args, **kwds):
    from JobBuilder import JobBuilder
    builder = JobBuilder()
    return builder(*args, **kwds)


# version
__id__ = "$Id$"

# End of file 
