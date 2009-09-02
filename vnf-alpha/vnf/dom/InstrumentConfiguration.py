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

    # the instrument for which this configuration is about
    target = pyre.db.reference(name='target', table=Instrument)

    componentsequence = pyre.db.varcharArray(
        name = 'componentsequence', length = 128, default = [] )

    components = vnf.dom.referenceSet(name='components')
    
    geometer = vnf.dom.geometer()

    configured = pyre.db.boolean(name='configured', default=False)

    pass # end of InstrumentConfiguration



# version
__id__ = "$Id$"

# End of file 
