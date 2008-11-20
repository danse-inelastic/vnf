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


from Instrument import Instrument


from OwnedObject import OwnedObject
class InstrumentConfiguration(OwnedObject):
    
    name = "instrumentconfigurations"
    
    import pyre.db
    import vnf.dom
    
    instrument = pyre.db.reference(name='instrument', table=Instrument)

    components = vnf.dom.referenceSet(name='components')
    
    geometer = vnf.dom.geometer()

    pass # end of InstrumentConfiguration



# version
__id__ = "$Id$"

# End of file 
