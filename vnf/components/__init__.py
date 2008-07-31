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


# version
__id__ = "$Id$"

# End of file 
