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
        from neutron_components import getHandler
        handler = getHandler(component)
        if handler:
            return handler(component)

    

# version
__id__ = "$Id$"

# End of file 
