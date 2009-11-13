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


from Lattice import Lattice


from AbstractOwnedObjectBase import AbstractOwnedObjectBase as base

class AtomicStructure(base):

    name = 'atomicstructures'

    import dsaw.db

    lattice = dsaw.db.reference(name='lattice', table=Lattice)
    atoms = dsaw.db.referenceSet(name='atoms')
    spacegroupno = dsaw.db.integer(name='spacegroupno')

    chemical_formula = dsaw.db.varchar(name='chemical_formula', length=1024)
    
    pass # end of AtomicStructure


# version
__id__ = "$Id$"

# End of file 
