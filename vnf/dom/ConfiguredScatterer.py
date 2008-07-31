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


class ConfiguredScatterer(OwnedObject):
    
    name = "configuredscatterers"
    
    import pyre.db

    scatterer_id = pyre.db.varchar( name = 'scatterer_id', length = 100 )
    scatterer_id.meta['tip'] = 'id of scatterer in the scatterer table'
    
    configuration_id = pyre.db.varchar( name = 'configuration_id', length = 100 )
    configuration_id.meta['tip'] = 'id of configuration in the "<scatterer>configuration" table'
    
    pass # end of ConfiguredScatterer


# version
__id__ = "$Id$"

# End of file 
