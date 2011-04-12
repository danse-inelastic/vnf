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


from pyre.inventory.Facility import Facility


class Geometer(Facility):


    def __init__(self, name):
        from vnf.components.Geometer import Geometer
        Facility.__init__(self, name=name, factory=Geometer, args=[name])

        return


    def _retrieveComponent(self, instance, componentName):
        from Geometer import Geometer
        geometer = Geometer(componentName)

        import pyre.parsing.locators
        locator = pyre.parsing.locators.simple('built-in')

        return geometer, locator
    

# version
__id__ = "$Id$"

# End of file 
