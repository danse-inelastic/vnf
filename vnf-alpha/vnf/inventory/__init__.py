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


def dataobject( *args, **kwds ):
    from DataObject import DataObject
    return DataObject( *args, **kwds )


def form( *args, **kwds ):
    from Form import Form
    return Form( *args, **kwds )


def geometer( *args, **kwds ):
    from Geometer import Geometer
    return Geometer( *args, **kwds )


def iworker(*args, **kwds):
    from IWorker import IWorker
    return IWorker(*args, **kwds)

import validators

# version
__id__ = "$Id$"

# End of file 
