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


def datadir( ):
    'path where data files are saved (relative to main.py)'
    import os
    return os.path.join( 'content', 'data' )


# version
__id__ = "$Id$"

# End of file 
