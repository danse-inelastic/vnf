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


class ARCSConfigurationApplyer:

    def __init__(self, instrument ):
        self.instrument = instrument
        return


    def apply(self, configuration):
        instrument = self.instrument
        components = instrument.components
        component0 = components[0]
        source = component0.realcomponent
        from vnf.dom.MonochromaticSource import MonochromaticSource
        assert isinstance( source, MonochromaticSource )
        return


    pass # end of ARCSConfigurationApplyer



# version
__id__ = "$Id$"

# End of file 
