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


from pyre.applications.Script import Script as base


class Templator(base):


    class Inventory(base.Inventory):

        import pyre.inventory

        name = pyre.inventory.str("name", default="test")
        name.meta['tip'] = 'the name of the application to generate'


    def main(self, *args, **kwds):
        name = self.inventory.name
        commands = [
            'mkdir %(name)s',
            'mkdir %(name)s/actors',
            'mkdir %(name)s/forms',
            'templator.py --template=project-makefile --filename=%(name)s/Make.mm --name=%(name)s --language=make',
            'templator.py --template=actor --filename=%(name)s/actors/%(name)s.odb --name=%(name)s --language=python',
            ]
        subs = locals()
        commands = map(lambda t: t % subs, commands)
        
        import os
        for cmd in commands:
            if os.system(cmd): raise RuntimeError, 'Command %(name)s failed' % cmd
            continue
        return


    def _init(self):
        super(Templator, self)._init()
        return



# version
__id__ = "$Id$"

# End of file
