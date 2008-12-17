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


from JobBuilder import JobBuilder as base
class Builder(base):

    from vnf.dom.AbInitio import AbInitio as Computation

    def render(self, computation, db=None, dds=None):
        self.db = db
        self.dds = dds
        
        files = []
        files += self._make_script(computation)
        
        return files
    

    def _make_pyscript(self, computation):
        engine = computation.engine
        handler = '_make_%s_pycode' % engine
        handler = getattr(self, handler)
        code = handler(computation)

        filename = 'run.py'
        path = self._path(filename)
        open(path, 'w').write('\n'.join(code))
        return filename
    
        
    def _make_script(self, computation):
        pyscript = self._make_pyscript(computation)
        cmds = [
            'source ~/.abinitio-env',
            'python %s' % pyscript
            ]
        path = self._path(self.shscriptname)
        open(path, 'w').write('\n'.join(cmds))
        return [pyscript, self.shscriptname]


    def _make_vasp_pycode(self, computation):
        code = []
        code += '''
from crystal.UnitCell import *
#from AbInitio.vasp.parsing.SystemPM import *
'''.split('\n')

        matter = computation.matter.dereference(self.db)

        cartesian_lattice = N.array(matter.cartesian_lattice)
        cartesian_lattice.shape = 3, 3
        cartesian_lattice = _postiveVolume(cartesian_lattice)
        vs = list(cartesian_lattice)
        vs = [tuple(v) for v in vs]
        code.append('uc=UnitCell()')
        code.append('vectors=%s' % (vs,))
        code.append('uc.setCellVectors(vectors)')

        nsites = len(matter.atom_symbols)
        
        coords = N.array(matter.fractional_coordinates)
        coords.shape = -1, 3
        assert len(coords)==nsites
        
        i = 0
        for atom, coord in zip(matter.atom_symbols, coords):
            coord = tuple(coord)
            line = 'site%d = Site(%s, Atom(symbol=%r))' % (i, coord, atom)
            code.append(line)
            i+=1
            continue
        code.append('sites = [%s]' % ','.join([ 'site%d' % i for i in range(nsites)]) )
        code.append('for i in range(%d):' % nsites)
        code.append('    uc.addSite(sites[i], sites[i].getAtom().symbol+str(i))')

        d = {
            'mattername': matter.chemical_formula,
            'ecutoff': computation.kineticEnergyCutoff,
            'xcf': computation.xcFunctional,
            'mhmesh': computation.monkhorstPackMesh,
            'qGrid': computation.qGrid,
            }
        callvasp = """
from AbInitio.AbiCalc import VaspCalc as VaspCalc
vc = VaspCalc.VaspCalc(unitcell = uc, kpts = %(mhmesh)s, ekincutoff=%(ecutoff)g, name=%(mattername)r, vaspcmd='vasp')
""" % d
        code += callvasp.split('\n')

        output = """
open('out.energy', 'w').write( '%s' % (vc.getPotEnergy(),) )
open('out.forces', 'w').write( '%s' % (vc.getForces(),) )
open('out.stress', 'w').write( '%s' % (vc.getStress(),) )
"""
        code += output.split('\n')
        return code


def _postiveVolume(vectors):
    vol = _volume(vectors)
    if vol == 0: raise RuntimeError
    if vol > 0: return vectors
    v0, v1, v2 = vectors
    return v0, v2, v1


def _volume(vectors):
    v0, v1, v2 = vectors
    return N.dot(v0, N.cross(v1, v2))


import numpy as N

# version
__id__ = "$Id$"

# End of file 
