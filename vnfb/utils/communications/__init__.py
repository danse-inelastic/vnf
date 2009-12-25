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


def announce(director, announcement, *args):
    import vnfb.components
    
    # create the announcer
    announcer = vnfb.components.announcer()
    director.configureComponent(announcer)
    announcer.init()
    
    # create the postman
    postman = vnfb.components.postman()
    director.configureComponent(postman)
    postman.init()

    # load the message template
    announcement = director.retrieveComponent(
        announcement, factory="announcement", args=args,
        vault=['announcements'])
    
    # send the email
    announcement.announce(director, announcer=announcer, postman=postman)
    
    return


# version
__id__ = "$Id$"

# End of file 
