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


from pyre.components.Component import Component


class Geometer(Component):


    def updateConfiguration(self, registry):
        listing = self._listing(registry)

        self.registry = listing

        self._debug.log( 'registry: %s' % self.registry )

        return []


    def __init__(self, name):
        Component.__init__(self, name, name)
        self.registry = []
        return


    def _listing(self, registry):
        listing = [
            (name, descriptor.value) for name, descriptor in registry.properties.iteritems()
            ]

        listing += [
            ("%s.%s" % (nodename, name), value)
            for nodename, node in registry.facilities.iteritems()
            for name, value in self._listing(node)
            ]

        return listing


# version
__id__ = "$Id$"

# End of file 
