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
        
        params = [
            ('name', matter.chemical_formula),
            ('ecutoff', computation.kineticEnergyCutoff),
            ('xcf', computation.xcFunctional),
            ('mpmesh', ','.join([str(i) for i in computation.monkhorstPackMesh]) ),
            ('unitcell', xyzfilename),
            ]
        cmds = [
            'source ~/.abinitio-env',
            'vaspapp.py ' + ' '.join(['-%s=%s' % (k,v) for k,v in params]),
            ]
        path = self._path(self.shscriptname)
        open(path, 'w').write('\n'.join(cmds))
        self._files.append(self.shscriptname)
        return


    def _makeXYZfile(self, crystal):
        from SampleAssemblyXMLBuilder import crystal2xyz
        contents = crystal2xyz(crystal)
        filename = 'matter.xyz'
        path = self._path(filename)
        open(path, 'w').write('\n'.join(contents))
        self._files.append(filename)
        return filename


# version
__id__ = "$Id$"

# End of file 
