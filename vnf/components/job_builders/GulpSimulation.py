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

    from vnf.dom.GulpSimulation import GulpSimulation as Computation

    def __init__(self, path):
        base.__init__(self, path)
        self.convertHistoryFile = False
        return

    def render(self, computation, db=None, dds=None):
        Computation = self.Computation

        # find out the file name of the gulp library file
        libptr = dds.abspath(computation, filename=Computation.LIBPOINTER_FILE)
        libname = open(libptr).read().strip()

        # two files need to be copied to job directory
        # 1. gulp.gin
        # 2. the library file
        files = [Computation.CONFIGURATION_FILE, libname]

        # copy files to job directory
        job = computation.job.dereference(db)
        for f in files:
            dds.copy(computation, f, job, f)
            
        # if the job outputs in DL_POLY format (necessary for trajectory analysis), mandate
        # conversion of the trajectory to netcdf format
        # 1. open the input file
        inputFilePath = dds.abspath(job, filename=Computation.CONFIGURATION_FILE)
        inputFileContents = open(inputFilePath).read()
        
        # 2. scan for string 'output history' and signal conversion if found
        if 'output history' in inputFileContents:
            self.convertHistoryFile = True

        # 3. add run.sh
        files.append( self._make_script1(computation) )
        files.append( self._make_script(computation) )
        return files


    def _make_script(self, computation):
        job = computation.job.dereference(self.db)
        np = job.numprocessors
        cmds = [
            '#!/usr/bin/env sh',
            '. ~/.gulp-env',
            'chmod +x %s' % self.shscript1name,
            'mpirun -np %d ./%s' % (np, self.shscript1name),
#            '',
#            "#setup brandon's python path",
#            'source /home/jbrkeith/.tools',
#            'history2Nc.py --historyFile=output.history --ncFile=output.nc'
            ]
        if self.convertHistoryFile:
            cmds += ['']
        cmds = ['',]   
        script = self.shscriptname
        path = self._path(script)
        open(path, 'w').write('\n'.join(cmds))
        return script
        

    shscript1name = 'run1.sh'
    def _make_script1(self, computation):
        Computation = self.Computation
        
        cmds = [
            '#!/usr/bin/env sh',
            '. ~/.gulp-env',
            'gulp < %s > gulp.out' % Computation.CONFIGURATION_FILE,
            '',
            ]
        script = self.shscript1name
        path = self._path(script)
        open(path, 'w').write('\n'.join(cmds))
        return script


# version
__id__ = "$Id$"

# End of file 
