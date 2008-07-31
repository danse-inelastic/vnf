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


def applyer( instrument ):
    global _applyers
    applyer = _applyers.get( instrument.id )
    if applyer is None:
        return default_applyer( instrument )
    return applyer( instrument )


class InstrumentConfigurationApplyer:

    def __init__(self, instrument ):
        self.instrument = instrument
        return


    def apply(self, configuration):
        instrument = self.instrument

        # update geometer
        try:
            geometer = configuration.geometer
            instrument.geometer.update( geometer )
        except AttributeError:
            pass

        components = configuration.components
        for component in components:
            for component0 in instrument.components:
                if component0.label == component.label:
                    #replace matched component
                    instrument.components[
                        instrument.components.index( component0 )] = component
                    continue
                continue
            continue
        return


    pass # end of InstrumentConfigurationApplyer

default_applyer = InstrumentConfigurationApplyer

from ARCSConfigurationApplyer import ARCSConfigurationApplyer
_applyers = {
    'ARCS': ARCSConfigurationApplyer
    }

# version
__id__ = "$Id$"

# End of file 
