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


from AtomicStructure import StructureTable


from Computation import Computation as base
class MaterialSimulation(base):

    # base class for all material simulations

    import dsaw.db
    matter = dsaw.db.reference(name='matter', table=StructureTable)
    
    pass # end of MaterialSimulation


# version
__id__ = "$Id$"

# End of file 
