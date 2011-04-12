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


class Form(Facility):


    def __init__(self, name = 'form', family=None, default=None, meta=None):
        Facility.__init__(self, name, family, default, None, (), meta)
        return


    def _retrieveComponent(self, instance, componentName, args):
        form = instance.retrieveComponent(
            componentName, factory='form', args=args, vault=['forms'])

        # if we were successful, return
        if form:
            form.aliases.append(self.name)
            return form, form.getLocator()

        # otherwise, try again
        return Facility._retrieveComponent(self, instance, componentName, args)

    pass # end of Form

# version
__id__ = "$Id$"

# End of file 
