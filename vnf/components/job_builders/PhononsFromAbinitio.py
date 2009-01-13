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
debug = journal.debug('phononsfromabinitio-jobbuilder')


from JobBuilder import JobBuilder as base
class Builder(base):

    from vnf.dom.PhononsFromAbinitio import PhononsFromAbinitio as Computation

    def render(self, computation, db=None, dds=None):
        self.computation = computation
        self._files = []
        self._make_script(computation)
        return self._files


    def getDependencies(self):
        computation = self.computation
        abinitio = computation.abinitio.dereference(self.db)
        job = abinitio.job.dereference(self.db)
        # !!!!!!!!
        return [job]
    

    def _make_script(self, computation):
        abinitio = computation.abinitio.dereference(self.db)
        abinitiojob = abinitio.job.dereference(self.db)

        job = computation.job.dereference(self.db)

        #need commands to copy files from abinitio job to the new job
        # !!!! Not good because it assumes the layout of the data directories
        # !!!! Not good because it assumes that "tmp" directory does not already exist
        copycmds = [
            'mkdir tmp',
            'mv * tmp/',
            'cp ../%s/* .' % abinitiojob.id,
            'mv tmp/* .',
            ]
        
        matter = abinitio.matter.dereference(self.db)
        xyzfilename = self._makeXYZfile(matter)

        computation_name = 'phonos for %s' % matter.chemical_formula
        computation_name = computation_name.replace(' ', '_')
        params = [
            ('name', computation_name),
            ('supersize', ','.join([str(i) for i in computation.supercell]) ),
            ('amplitude', computation.displacementAmplitude),
            ('qgridsize', ','.join([str(i) for i in computation.qGrid]) ),
            ('unitcell', xyzfilename),
            ]
        cmds = copycmds + [
            'source ~/.abinitio-env',
            'phonapp.py ' + ' '.join(['-%s=%s' % (k,v) for k,v in params]),
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
