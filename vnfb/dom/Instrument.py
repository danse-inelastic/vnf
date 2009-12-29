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



class Instrument(object):
    
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



from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    components = InvBase.d.referenceSet(name = 'components', targettype=Component)
    
    import dsaw.db
    componentsequence = dsaw.db.varcharArray(
        name = 'componentsequence', length = 128, default = [] )

    category = dsaw.db.varchar( name = 'category', length = 64 )

    import vnf.dom
    geometer = vnf.dom.geometer()

    long_description = dsaw.db.varchar( name = 'long_description', length = 8192 )

    status = dsaw.db.varchar(name='status', length=32, default='online')
    

    dbtablename = "instruments"
    

# ????
def inittable(db):
    from instruments import initall
    return initall(db)


# version
__id__ = "$Id$"

# End of file 
