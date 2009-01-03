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


def new_id( director ):
    #new token
    token = director.idd.token()
    uniquename = '%s' % (token.locator,)
    return uniquename


def empty_id( id ):
    return id in [None, 'None', '']


def nullpointer( p ):
    return p is None


def announce(director, announcement, *args):
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
        announcement, factory="announcement", args=args,
        vault=['announcements'])
    
    # send the email
    announcement.announce(director, announcer=announcer, postman=postman)
    
    return

# version
__id__ = "$Id$"

# End of file 
