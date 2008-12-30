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


from vnf import extensions


def clerk():    
    from Clerk import Clerk as base, findClerks
    Clerks = findClerks(extensions)

    from _extend_class import subclassOf
    Clerk = subclassOf([base]+Clerks)

    from Clerk import DeepCopier as base, findDeepCopiers
    DeepCopiers = findDeepCopiers(extensions)
    DeepCopier = subclassOf([base]+DeepCopiers)
    
    Clerk.DeepCopier = DeepCopier

    return Clerk( 'clerk', 'clerk' )


def accesscontrol():
    from AccessControl import AccessControl
    return AccessControl()


def scribe():
    from Scribe import Scribe
    return Scribe( 'scribe', 'scribe' )


def usersFromDB():
    from UsersFromDB import UsersFromDB
    return UsersFromDB('usersFromDB')


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


def retrieveresults(*args, **kwds):
    from ComputationResultsRetriever import ComputationResultsRetriever
    retriever = ComputationResultsRetriever()
    return retriever(*args, **kwds)


# version
__id__ = "$Id$"

# End of file 
