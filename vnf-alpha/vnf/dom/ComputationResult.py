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


from Table import Table
class ComputationResult(Table):

    import dsaw.db
    origin = dsaw.db.versatileReference(name='origin', tableRegistry=tableRegistry)
    
    pass # end of PhononDOS


# version
__id__ = "$Id$"

# End of file 
