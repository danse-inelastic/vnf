#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.services.TCPService import TCPService


class JobStatusUpdater(TCPService):


    class Inventory(TCPService.Inventory):

        import pyre.inventory
        from pyre.units.time import hour

        sleep = pyre.inventory.dimensional("sleep", default=0.5*hour)

        from vnf.services.Pickler import Pickler
        marshaller = pyre.inventory.facility(
            "marshaller", factory=Pickler, args = ['jsu-pickler'])


    def generateClientConfiguration(self, registry):
        """update the given registry node with sufficient information to grant access to clients"""

        import pyre.parsing.locators
        locator = pyre.parsing.locators.simple('service')

        # get the inherited settings
        TCPService.generateClientConfiguration(self, registry)

        # record the marshaller name
        registry.setProperty('marshaller', self.marshaller.name, locator)

        # get the marshaller to record his configuration
        marshaller = registry.getNode(self.marshaller.name)
        self.marshaller.generateClientConfiguration(marshaller)

        return


    def onTimeout(self, selector):
        import time
        self._info.log("thump")
        return True


    def onReload(self, *unused):
        return self.userManager.onReload()


    def __init__(self, name=None):
        if name is None:
            name = "jsu"

        TCPService.__init__(self, name)

        return


    def _configure(self):
        TCPService._configure(self)
        self.marshaller = self.inventory.marshaller
        return



# version
__id__ = "$Id$"

# End of file 
