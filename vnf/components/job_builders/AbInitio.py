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


import journal
debug = journal.debug('abinitio-jobbuilder')


from JobBuilder import JobBuilder as base
class Builder(base):

    from vnf.dom.AbInitio import AbInitio as Computation

    def render(self, computation, db=None, dds=None):
        self.db = db
        self.dds = dds
        
        self._files = []
        self._make_script(computation)
        
        return self._files
    

    def _make_script(self, computation):
        engine = computation.engine
        handler = '_make_%s_script' % engine
        handler = getattr(self, handler)
        handler(computation)
        return


    def _make_vasp_script(self, computation):
        matter = computation.matter.dereference(self.db)
        xyzfilename = self._makeXYZfile(matter)
        xcFunctional = computation.xcFunctional
        xcf = _xcf[xcFunctional]
        
        params = [
            ('name', matter.chemical_formula or computation.short_description or computation.id),
            ('ecutoff', computation.kineticEnergyCutoff),
            ('xcf', xcf),
            ('mpmesh', ','.join([str(i) for i in computation.monkhorstPackMesh]) ),
            ('unitcell', xyzfilename),
            ('generateInputsOnly', computation.generateInputsOnly),
            ]
        cmds = [
            'source ~/.abinitio-env',
            'vaspapp.py ' + ' '.join(['-%s=%s' % (k,v) for k,v in params]),
            ]
        path = self._path(self.shscriptname)
        open(path, 'w').write('\n'.join(cmds))
        self._files.append(self.shscriptname)

        if not computation.generateInputsOnly:
            # copy vasp input files if they alreday exist
            dds = self.dds
            files = [
                'INCAR',
                'POSCAR',
                'POTCAR',
                'KPOINTS',
                ]
            job = computation.job.dereference(self.db)
            import shutil, os
            for f in files:
                src = dds.abspath(computation, f)
                dest = dds.abspath(job, f)
                debug.log('copying file %s to %s' % (src, dest))
                if os.path.exists(src):
                    shutil.copyfile(src, dest)
                    self._files.append(f)
                else:
                    debug.log('file %s does not exist' % src)
                continue
            
        return


    def _makeXYZfile(self, crystal):
        from SampleAssemblyXMLBuilder import crystal2xyz
        contents = crystal2xyz(crystal)
        filename = 'matter.xyz'
        path = self._path(filename)
        open(path, 'w').write('\n'.join(contents))
        self._files.append(filename)
        return filename

_xcf = {
    'PAW-PBE': 'pawpbe',
    'PAW-GGA': 'pawgga',
    'PAW-LDA': 'pawlda',
    'USPP-GGA': 'usppgga',
    'USPP-LDA': 'uspplda',
    }

# version
__id__ = "$Id$"

# End of file 
