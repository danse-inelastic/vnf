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


"""
This script creates some prebuilt neutron instruments for vnf.

Those prebuilt instruments are under vnfb/dom/neutron_experiment_simulations/instruments/
Two forms of instrument files are accepted:
 1. instrument = dictionary of information about the instrument. eg. Test.py
 2. createInstrument = factory method that create an instrument in the db given this
    application as the directory. eg. ARCS_beam.py

It should be easy to make this app to accept arbitrary python file (so it is
not limited to the files in vnfb/dom/neutron_experiment_simulations/instruments
"""


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
