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
    return tables


def subclassesOf( base ):
    from _all_tables import children
    return children( base )


# version
__id__ = "$Id$"

# End of file 
