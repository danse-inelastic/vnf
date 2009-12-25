# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2008-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Computation import Computation as base
class MaterialSimulation(base):

    # base class for all material simulations

    import dsaw.db
    matter = dsaw.db.versatileReference(name='matter')
    
    pass # end of MaterialSimulation


# version
__id__ = "$Id$"

# End of file 
