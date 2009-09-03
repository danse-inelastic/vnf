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


from AbstractOwnedObjectBase import AbstractOwnedObjectBase as base
class ComputationResult(base):

    import dsaw.db
    origin = dsaw.db.versatileReference(name='origin')
    
    pass # end of PhononDOS


# version
__id__ = "$Id$"

# End of file 
