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


class DbApp(base):


    class Inventory(base.Inventory):

        import pyre.inventory

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", default='clerk')
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        import pyre.idd
        idd = pyre.inventory.facility('idd-session', factory=pyre.idd.session, args=['idd-session'])
        idd.meta['tip'] = "access to the token server"


    def main(self, *args, **kwds):
        orm = self.clerk.orm

        models = self._readModels()
        for model in models:
            print ' * saving model %s... ' % model.short_description
            orm.save(model.matter)
            orm.save(model, save_not_owned_referred_object=0)
            continue
        return


    def _convertToModel(self, module):
        if module.lattice_type not in ['bcc', 'fcc']: return

        ltype = module.lattice_type
        handler = '_convert%sModel' % ltype
        print ' * converting %s ...' % module.__name__
        return getattr(self, handler)(module)


    def _convertbccModel(self, module):
        atom1 = Atom(module.element)
        atom2 = Atom(module.element, [0.5,0.5,0.5])
        atoms = [atom1, atom2]
        a = module.a
        lattice = Lattice(a=a,b=a,c=a, alpha=90, beta=90, gamma=90)
        description = '%s %s at %sK' % (module.lattice_type, module.element, module.temperature)
        struct = Structure(lattice=lattice, sgid=229, atoms=atoms, description=description)

        model = BvKModel()
        model.matter = struct
        model.short_description = 'bvk model of %s from literature' % description
        try:
            model.long_description = module.details
        except AttributeError:
            pass
        try:
            model.reference = module.reference
        except AttributeError:
            pass

        bonds = []
        for bond, fc in module.force_constants.iteritems():
            vec = numpy.array(map(float, bond))/2.
            bvkbond = BvKBond()
            bvkbond.matter = struct
            bvkbond.A = bvkbond.B = 0
            bvkbond.Boffset = vec
            try:
                bvkbond.force_constant_matrix = eval('bcc%s' % bond)(fc)
            except:
                import traceback
                raise RuntimeError, 'failed to convert force constant matrix. module %s, bond %s, fc %s\n%s' % (module.__name__, bond, fc, traceback.format_exc())
            bonds.append(bvkbond)
            continue

        model.bonds = bonds
        return model
    
        
    def _convertfccModel(self, module):
        atom1 = Atom(module.element)
        atom2 = Atom(module.element, [0.5,0.5,0])
        atom3 = Atom(module.element, [0.5,0,0.5])
        atom4 = Atom(module.element, [0,0.5,0.5])
        atoms = [atom1, atom2, atom3, atom4]
        a = module.a
        lattice = Lattice(a=a,b=a,c=a, alpha=90, beta=90, gamma=90)
        description = '%s %s at %s' % (module.lattice_type, module.element, module.temperature)
        struct = Structure(lattice=lattice, sgid=225, atoms=atoms, description=description)

        model = BvKModel()
        model.matter = struct
        model.short_description = 'bvk model of %s from literature' % description
        try:
            model.long_description = module.details
        except AttributeError:
            pass
        try:
            model.reference = module.reference
        except AttributeError:
            pass

        bonds = []
        for bond, fc in module.force_constants.iteritems():
            vec = numpy.array(map(float, bond))/2.
            bvkbond = BvKBond()
            bvkbond.matter = struct
            bvkbond.A = bvkbond.B = 0
            bvkbond.Boffset = vec
            try:
                bvkbond.force_constant_matrix = eval('fcc%s' % bond)(fc)
            except:
                import traceback
                raise RuntimeError, 'failed to convert force constant matrix. module %s, bond %s, fc %s\n%s' % (module.__name__, bond, fc, traceback.format_exc())
            bonds.append(bvkbond)
            continue

        model.bonds = bonds
        return model


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
        return ['../config']



def fcc110(fc):
    xx = fc['xx']
    xy = fc['xy']
    zz = fc['zz']
    return [[xx, xy, 0],
            [xy, xx, 0],
            [0, 0, zz]]


def fcc200(fc):
    xx = fc['xx']
    yy = fc['yy']
    return [[xx, 0, 0],
            [0, yy, 0],
            [0, 0, yy]]


def fcc211(fc):
    xx = fc['xx']
    yy = fc['yy']
    xz = fc['xz']
    yz = fc['yz']
    return [[xx, xz, xz],
            [xz, yy, yz],
            [xz, yz, yy]]


fcc220 = fcc110


def fcc310(fc):
    xx = fc['xx']
    yy = fc['yy']
    zz = fc['zz']
    xy = fc['xy']
    return [[xx, xy, 0],
            [xy, yy, 0],
            [0, 0, zz]]


def fcc222(fc):
    xx = fc['xx']
    xy = fc['xy']
    return [[xx, xy, xy],
            [xy, xx, xy],
            [xy, xy, xx]]


def fcc321(fc):
    xx = fc['xx']
    yy = fc['yy']
    zz = fc['zz']
    yz = fc['yz']
    xz = fc['xz']
    xy = fc['xy']
    return [[xx, xy, xz],
            [xy, yy, yz],
            [xz, yz, zz]]


fcc400 = fcc200




def bcc111(fc):
    xx = fc['xx']
    xy = fc['xy']
    return [[xx, xy, xy],
            [xy, xx, xy],
            [xy, xy, xx]]


def bcc200(fc):
    xx = fc['xx']
    yy = fc['yy']
    return [[xx, 0, 0],
            [0, yy, 0],
            [0, 0, yy]]


def bcc220(fc):
    xx = fc['xx']
    xy = fc['xy']
    zz = fc['zz']
    return [[xx, xy, 0],
            [xy, xx, 0],
            [0, 0, zz]]


def bcc311(fc):
    xx = fc['xx']
    yy = fc['yy']
    yz = fc['yz']
    xz = fc['xz']
    return [[xx, xz, xz],
            [xz, yy, yz],
            [xz, yz, yy]]


bcc222 = bcc111
bcc400 = bcc200

def bcc133(fc):
    xx = fc['xx']
    yy = fc['yy']
    yz = fc['yz']
    xy = fc.get('xy') or fc['xz']
    return [[xx, xy, xy],
            [xy, yy, yz],
            [xy, yz, yy]]


def bcc420(fc):
    xx = fc['xx']
    yy = fc['yy']
    zz = fc['zz']
    xy = fc['xy']
    return [[xx, xy, 0],
            [xy, yy, 0],
            [0, 0, zz]]


from vnfb.dom.material_simulations.BvKModel import BvKModel, BvKBond
from matter import Structure, Lattice, Atom
from bvk.find_force_constant_tensor_constraints import findForceContantTensorConstraints
import numpy


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
