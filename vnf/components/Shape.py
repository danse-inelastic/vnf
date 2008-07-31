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
    uniquename = '%s-%s-%s' % (token.locator, token.tid, token.date)
    return uniquename


def new_shape( director ):
    from vnf.dom.Shape import Shape
    record = Shape()

    id = new_id( director )
    record.id = id

    import time
    record.date = time.ctime()

    director.clerk.newRecord( record )
    
    return record



from misc import new_id


# version
__id__ = "$Id$"

# End of file 
