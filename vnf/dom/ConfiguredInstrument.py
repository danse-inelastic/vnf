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


class ConfiguredInstrument(OwnedObject):
    
    name = "configuredinstruments"
    
    import pyre.db

    instrument_id = pyre.db.varchar( name = 'instrument_id', length = 100 )
    instrument_id.meta['tip'] = 'id of instrument in the instrument table'
    
    configuration_id = pyre.db.varchar( name = 'configuration_id', length = 100 )
    configuration_id.meta['tip'] = 'id of configuration in the "<instrument>configuration" table'
    
    pass # end of ConfiguredInstrument


# version
__id__ = "$Id$"

# End of file 
