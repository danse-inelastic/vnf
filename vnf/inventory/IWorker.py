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
class Dummy(Component):
    def __init__(self, name='dummy', facility='iworker'):
        Component.__init__(self, name, facility)
        

from pyre.inventory.Facility import Facility


class IWorker(Facility):


    def __init__(self, name = 'iworker', family=None, default=Dummy(), meta=None):
        Facility.__init__(self, name, family, default, None, (), meta)
        return


    def _retrieveComponent(self, instance, componentName, args):
        worker = instance.retrieveComponent(
            componentName, factory='iworker', args=args, vault=['iworkers'])

        # if we were successful, return
        if worker:
            worker.aliases.append(self.name)
            return worker, worker.getLocator()

        # otherwise, try again
        return Facility._retrieveComponent(self, instance, componentName, args)

    pass # end of IWorker

# version
__id__ = "$Id$"

# End of file 
