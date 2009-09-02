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


from pyre.applications.Script import Script


class CreateInstrumentApp(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnf.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        import pyre.idd
        idd = pyre.inventory.facility('idd-session', factory=pyre.idd.session, args=['idd-session'])
        idd.meta['tip'] = "access to the token server"

        instrument = pyre.inventory.str(name='instrument')


    def main(self, *args, **kwds):

        self.db.autocommit(True)

        self._createInstrument(self.instrument)
        return


    def _createInstrument(self, instrument):
        package = 'vnf.dom.instruments'
        module = _import('%s.%s' % (package, instrument))
        module.create(self.db)
        return
    

    def __init__(self):
        Script.__init__(self, 'createInstrument')
        self.db = None
        return


    def _configure(self):
        Script._configure(self)
        self.clerk = self.inventory.clerk
        self.clerk.director = self
        return


    def _init(self):
        Script._init(self)

        self.db = self.clerk.db
        self.idd = self.inventory.idd
        self.instrument = self.inventory.instrument

        # initialize table registry
        import vnf.dom
        vnf.dom.register_alltables()

        # id generator
        def guid(): return '%s' % self.idd.token().locator
        import vnf.dom
        vnf.dom.set_idgenerator( guid )
        return


    def _getPrivateDepositoryLocations(self):
        return ['../config']
    


def _import(package):
    return __import__(package, {}, {}, [''])


def main():
    import journal
    journal.debug('db').activate()
    app = CreateInstrumentApp()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
