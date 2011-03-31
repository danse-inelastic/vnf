#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from luban.applications.UIApp import UIApp as base


class DbApp(base):


    class Inventory(base.Inventory):

        import pyre.inventory

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", default='clerk')
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        announcement = pyre.inventory.str('announcement')


    def main(self, *args, **kwds):
        announcement = self.inventory.announcement

        kwds = {}
        for k, v in self.inventory.__dict__.iteritems():
            if k.startswith('_'): continue
            if hasattr(self.Inventory, k): continue
            kwds[k] = v
            continue

        from vnf.utils.communications import announce
        announce(self, announcement, **kwds)
        return


    # accept arbitrary inputs
    def updateConfiguration(self, registry):
        listing = self._listing(registry)
        if listing:
            for k, v in listing:
                setattr(self.inventory, k, v)        
        return []

    
    def _listing(self, registry):
        if not registry: return []
        listing = [
            (name, descriptor.value) for name, descriptor in registry.properties.iteritems()
            ]

        listing += [
            ("%s.%s" % (nodename, name), value)
            for nodename, node in registry.facilities.iteritems()
            for name, value in self._listing(node)
            ]

        return listing


    def __init__(self):
        base.__init__(self, 'announce')
        return


    def _getPrivateDepositoryLocations(self):
        return ['../config', '../content/components']



def main():
    import journal
    journal.debug('db').activate()
    app = DbApp()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
