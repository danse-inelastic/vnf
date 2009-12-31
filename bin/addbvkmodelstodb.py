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


# orm in effect
## from bvk.orm.BvKModel import BvKModel
## from bvk.orm.BvKBond import BvKBond
## from matter.orm.Lattice import Lattice
## from matter.orm.Atom import Atom
## from matter.orm.Structure import Structure


from luban.applications.UIApp import UIApp as base


class DbApp(base):


    class Inventory(base.Inventory):

        import pyre.inventory



    def main(self, *args, **kwds):
        domaccess = self.retrieveDOMAccessor('material_simulations/phonon_calculators/bvk')
        orm = domaccess.orm

        models = self._readModels()
        for model in models:
            print ' * saving model %s... ' % model.short_description
            orm.save(model.matter)
            orm.save(model, save_not_owned_referred_object=0)
            continue
        return


    def _convertToModel(self, module):
        from bvk.bvkmodels.converttobvkmodelobject import module2model
        return module2model(module)


    def _readModels(self):
        modules = self._getModules()
        models = []
        for mod in modules:
            model = self._convertToModel(mod)
            if model:
                models.append(model)
            continue
        return models


    def _getModules(self):
        from bvk import bvkmodels
        f = bvkmodels.__file__

        import os
        d = os.path.dirname(f)

        entries = os.listdir(d); modules = []
        for entry in entries:
            # skip private modules
            if entry.startswith('_'): continue
            # skip directories
            p = os.path.join(d, entry)
            if os.path.isdir(p): continue
            # skip anything not python
            if not entry.endswith('.py'): continue
            #
            name = entry[:-3]
            m = __import__('bvk.bvkmodels.%s' % name, {}, {}, [''])
            modules.append(m)
            continue
        return modules            


    def __init__(self):
        base.__init__(self, 'addbvkmodelstodb')
        return


    def _getPrivateDepositoryLocations(self):
        return ['../config', '../content/components', '/tmp/luban/services']



def main():
    import journal
    journal.debug('db').activate()
    app = DbApp()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
