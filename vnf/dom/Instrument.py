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



from OwnedObject import OwnedObject
class Instrument(OwnedObject):
    
    name = "instruments"
    
    import vnf.dom
    components = vnf.dom.referenceSet( name = 'components' )
    
    import pyre.db
    componentsequence = pyre.db.varcharArray(
        name = 'componentsequence', length = 128, default = [] )

    category = pyre.db.varchar( name = 'category', length = 64 )

    import vnf.dom
    geometer = vnf.dom.geometer()
    
    pass # end of Instrument



# version
__id__ = "$Id$"

# End of file 
