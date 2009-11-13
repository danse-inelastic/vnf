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


class Lattice(GloballyReferrable, WithID):

    name = 'lattices'

    import dsaw.db

    a = dsaw.db.real(name = 'a' )
    b = dsaw.db.real(name = 'b' )
    c = dsaw.db.real(name = 'c' )

    alpha = dsaw.db.real(name = 'alpha' )
    beta = dsaw.db.real(name = 'beta' )
    gamma = dsaw.db.real(name = 'gamma' )
    
    pass # end of Lattice


# version
__id__ = "$Id$"

# End of file 
