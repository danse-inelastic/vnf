# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# utilities to communicate with users, etc. eg emails


def announce(director, announcement, *args, **kwds):
    import vnf.components
    
    # create the announcer
    announcer = vnf.components.announcer()
    director.configureComponent(announcer)
    announcer.init()
    
    # create the postman
    postman = vnf.components.postman()
    director.configureComponent(postman)
    postman.init()

    # load the message template
    announcement = director.retrieveComponent(
        announcement, factory="announcement", args=args, kwds=kwds,
        vault=['announcements'])

    #
    if announcement is None:
        curator_dump = director._dumpCurator()
        raise RuntimeError, 'unable to retrieve announcement. Curator dump %s' % curator_dump

    # send the email
    announcement.announce(director, announcer=announcer, postman=postman)
    
    return


# version
__id__ = "$Id$"

# End of file 
