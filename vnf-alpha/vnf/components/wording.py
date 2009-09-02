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


def present_be( n ):
    if n > 1: return 'are'
    return 'is'


def plural1( n ):
    if n>1: return 's'
    return ''

def plural2( n ):
    if n>1: return 'ies'
    return 'y'

def plural( n, ending = '' ):
    f = { '': plural1,
          'y': plural2,
        }
    return f[ending](n)


# version
__id__ = "$Id$"

# End of file 
