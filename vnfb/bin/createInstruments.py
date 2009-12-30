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


class CreateInstrumentsApp(base):


    class Inventory(base.Inventory):

        import pyre.inventory
        instruments = pyre.inventory.list(name='instruments')


    def main(self, *args, **kwds):
        instruments = self.inventory.instruments
        self._createInstruments(instruments)
        return


    def _createInstruments(self, instruments):
        for instrument in instruments:
            self._createInstrument(instrument)
        return


    def _createInstrument(self, instrument):
        module = self._importInstrumentModule(instrument)
        
        fkey = 'createInstrument'
        if hasattr(module, fkey):
            f = getattr(module, fkey)
            return f(self)

        instrument = getattr(module, 'instrument')
        
        orm = self.clerk.orm
        from vnfb.dom.neutron_experiment_simulations.instruments import createInstrument
        createInstrument(instrument, orm)
        
        return


    def _importInstrumentModule(self, name):
        n = 'neutron_experiment_simulations.instruments.%s' % name
        from vnfb.dom import _import
        return _import(n)


    def _getPrivateDepositoryLocations(self):
        return ['../config', '../content/components', '/tmp/luban-servicces']
    


def main():
    import journal
    journal.debug('db').activate()
    app = CreateInstrumentsApp('createInstruments')
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
