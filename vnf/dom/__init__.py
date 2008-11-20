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


def create_referenceset_table(db):
    from _referenceset import _ReferenceTable
    db.createTable( _ReferenceTable )
    return


def set_idgenerator( generator ):
    import idgenerator
    idgenerator.generator = generator
    return


def referenceSet(**kwds):
    from ReferenceSet import ReferenceSet
    return ReferenceSet(**kwds)


def geometer(**kwds):
    from Geometer import Geometer
    return Geometer(**kwds)


def alltables():
    from _all_tables import tables
    return tables()


def kerneltables():
    all = alltables()
    from ScatteringKernel import ScatteringKernel
    return filter( lambda t: issubclass(t, ScatteringKernel), all )


def mattertables():
    all = alltables()
    from MatterBase import MatterBase
    return filter( lambda t: issubclass(t, MatterBase), all )


def computationtables():
    all = alltables()
    from Computation import Computation as base
    return filter( lambda t: issubclass(t, base), all )


def materialsimulationtables():
    all = alltables()
    from MaterialSimulation import MaterialSimulation as base
    return filter( lambda t: issubclass(t, base), all )


def materialmodelingtables():
    all = alltables()
    from MaterialModeling import MaterialModeling as base
    return filter( lambda t: issubclass(t, base), all )


def subclassesOf( base ):
    from _all_tables import children
    return children( base )


def register_alltables():
    tables = alltables()
    from registry import tableRegistry
    for t in tables: tableRegistry.register( t )
    return


# version
__id__ = "$Id$"

# End of file 
