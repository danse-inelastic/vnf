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



from AbstractOwnedObjectBase import AbstractOwnedObjectBase as base
class Instrument(base):
    
    name = "instruments"
    
    import vnf.dom
    components = vnf.dom.referenceSet( name = 'components' )
    
    import dsaw.db
    componentsequence = dsaw.db.varcharArray(
        name = 'componentsequence', length = 128, default = [] )

    category = dsaw.db.varchar( name = 'category', length = 64 )

    import vnf.dom
    geometer = vnf.dom.geometer()

    long_description = dsaw.db.varchar( name = 'long_description', length = 8192 )

    status = dsaw.db.varchar(name='status', length=32, default='online')
    
    pass # end of Instrument


def inittable(db):
    from instruments import initall
    return initall(db)


# version
__id__ = "$Id$"

# End of file 
