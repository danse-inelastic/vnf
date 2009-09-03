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

from ComputationResult import ComputationResult
class PhononDOS(ComputationResult):

    name = 'phonondoses'

    import dsaw.db
    matter = dsaw.db.versatileReference(name='matter')
    
    datafiles = [
        'data.idf',
        ]
    
    pass # end of PhononDOS


# version
__id__ = "$Id$"

# End of file 
