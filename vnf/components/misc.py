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


def defaultServer(director):
    from vnf.dom.Server import Server
    servers = director.clerk.db.fetchall(Server)
    return servers[0]


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

def partition(alist):
    '''partitions a list into several lists, each list containing the same type of element'''
    distinctKinds=[]
    partitionList=[]
    alist.sort()
    for item in alist:
        if item in distinctKinds:
            partitionList[-1].append(item)
        else:
            partitionList.append([item])
            distinctKinds.append(item)
    return partitionList
    
if __name__=='__main__':
    print partition([3,3,4,4,5,8,'x','x','h',3,2,5,5])

# version
__id__ = "$Id$"

# End of file 
