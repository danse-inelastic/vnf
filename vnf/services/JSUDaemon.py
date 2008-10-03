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


from pyre.applications.ServiceDaemon import ServiceDaemon


class Daemon(ServiceDaemon):


    class Inventory(ServiceDaemon.Inventory):

        import pyre.inventory

        name = pyre.inventory.str('name', default='jsu')


    def createComponent(self):
        name = self.inventory.name

        # instantiate the service
        from vnf.services.JobStatusUpdater import JobStatusUpdater
        service = JobStatusUpdater(self.inventory.name)

        # register a weaver
        service.weaver = self.weaver

        return service


    def __init__(self, name=None):
        if name is None:
            name = 'jsu-harness'

        ServiceDaemon.__init__(self, name)
        self._debug.log( name )
        
        return


# version
__id__ = "$Id$"

# End of file 
