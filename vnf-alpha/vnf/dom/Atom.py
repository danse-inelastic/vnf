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


from dsaw.db.GloballyReferrable import GloballyReferrable
from dsaw.db.WithID import WithID


class Atom(GloballyReferrable, WithID):

    name = 'atoms'

    import dsaw.db

    element = dsaw.db.varchar( name = 'element', length=8 )
    xyz = dsaw.db.doubleArray(name='xyz', shape=3)
    occupancy = dsaw.db.real(name='occupancy', default=1)
    
    pass # end of Atom


# version
__id__ = "$Id$"

# End of file 
