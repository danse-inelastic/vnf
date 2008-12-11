# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Retriever import Retriever as base

class Retriever(base):


    from vnf.dom.NeutronExperiment import NeutronExperiment as Computation

    def retrieve(self):
        director = self.director

        simulation = self.simulation
        instrument = director.clerk.dereference(simulation.instrument)
        components = director.clerk.dereference(instrument.components)
        for name, component in components:
            self.dispatch(component)
        return


    def dispatch(self, component):
        handler = self._getHandler(component)
        return handler(component)


    def _getHandler(self, component):
        type = component.__class__.__name__
        module = 'neutron_components.%s' % type
        module = __import__(module, {}, {}, [''])
        return module.retrieve
    

# version
__id__ = "$Id$"

# End of file 
