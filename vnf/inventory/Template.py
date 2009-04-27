# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.inventory.Facility import Facility


class Template(Facility):


    def __init__(self, name = 'template', family=None, default=None, meta=None):
        Facility.__init__(self, name, family, default, None, (), meta)
        return


    def _retrieveComponent(self, instance, componentName, args):
        template = instance.retrieveComponent(
            componentName, factory='template', args=args, vault=['templates'])

        # if we were successful, return
        if template:
            template.aliases.append(self.name)
            return template, template.getLocator()

        # otherwise, try again
        return Facility._retrieveComponent(self, instance, componentName, args)

    pass # end of Template

# version
__id__ = "$Id$"

# End of file 
