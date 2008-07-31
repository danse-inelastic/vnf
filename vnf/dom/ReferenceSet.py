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


from Table import Table


class ReferenceSet(Table):


    import pyre.db
    
    # columns
    id = pyre.db.varchar( name = 'id', length = 100 )
    id.constraints = 'PRIMARY KEY'
    
    localkey = pyre.db.varchar( name = 'localkey', length = 100 )
    remotekey = pyre.db.varchar( name = 'remotekey', length = 100 )

    pass # end of ReferenceSet


# version
__id__ = "$Id$"

# End of file 
