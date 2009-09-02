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


def applyer( scatterer ):
    return default_applyer( scatterer )


class ScattererConfigurationApplyer:

    def __init__(self, scatterer ):
        self.scatterer = scatterer
        return


    def apply(self, configuration):
        scatterer = self.scatterer

        # scatterer is a container of matter and shape
        matter = scatterer.matter.realmatter
        shape = scatterer.shape.realshape
        
        # the configuration is also a container of matter and shape
        # if it exists
        if configuration is None: return

        matter_id = configuration.matter_id
        if not empty_id(matter_id):
            # need implementation here
            pass

        
        return


    pass # end of ScattererConfigurationApplyer

default_applyer = ScattererConfigurationApplyer


from misc import empty_id

# version
__id__ = "$Id$"

# End of file 
