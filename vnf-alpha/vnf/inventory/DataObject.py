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


from pyre.inventory.Facility import Facility


class DataObject(Facility):


    def __init__(self, family=None, default=None, meta=None):
        Facility.__init__(self, 'dataobject', family, default, None, (), meta)
        return


    def _retrieveComponent(self, instance, componentName, args):
        dataobject = instance.retrieveComponent(
            componentName, factory='dataobject', args=args, vault=['dataobjects'])

        # if we were successful, return
        if dataobject:
            dataobject.aliases.append(self.name)
            return dataobject, dataobject.getLocator()

        # otherwise, try again
        return Facility._retrieveComponent(self, instance, componentName, args)

    pass # end of DataObject

# version
__id__ = "$Id$"

# End of file 
