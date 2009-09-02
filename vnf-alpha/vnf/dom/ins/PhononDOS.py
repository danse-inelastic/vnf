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

from registry import tableRegistry

from OwnedObject import OwnedObject
from ComputationResult import ComputationResult
class PhononDOS(OwnedObject, ComputationResult):

    name = 'phonondoses'

    import pyre.db
    matter = pyre.db.versatileReference(name='matter', tableRegistry=tableRegistry)
    
    datafiles = [
        'data.idf',
        ]
    
    pass # end of PhononDOS


# version
__id__ = "$Id$"

# End of file 
