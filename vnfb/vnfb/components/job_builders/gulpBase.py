
import journal
debug = journal.debug('atomsim')


from vnfb.components.JobBuilder import JobBuilder as base

class Builder(base):

    def __init__(self, name, path):
        base.__init__(self, name, path)
    
    def _make_script(self, computation, db=None, dds = None):
        job = computation.getJob(self.db)
        #server = director.clerk.dereference(job.server)
        server = job.server.dereference(db)
        server_jobpath = dds.abspath(job, server=server)
        np = job.numprocessors()
        #octopod
        if job.server.id=='server000':
            cmds = [
                '#!/usr/bin/env bash',
                '. ~/.gulp-env',
                'mpirun -np %d gulp < %s > %s' % (np, computation.inputFile, computation.output_filename),
                '',
                ]
            if self.convertHistoryFile:
                cmds += [
                'conversionTasks.py -convertHistoryFile=True -historyFile=gulp.his -ncFile=gulp.nc',
                'if [ -e gulp.nc ]; then rm gulp.his; fi',
                         ] 
        #foxtrot md
        elif job.server.id=='server002':
            cmds = [
                '#!/usr/bin/env bash',
                'source /home/jbrkeith/.bash_profile',
                #'. ~/.vnf',
                #'. ~/.gulp-env',
                'mpirun -np %d gulp_openmpi < %s > %s' % (np, computation.inputFile, computation.output_filename),
                '',
                ]
            if self.convertHistoryFile:
                cmds += [
                '/usr/local/python-2.6.2/bin/python2.6 /home/jbrkeith/dv/tools/pythia-0.8/bin/conversionTasks.py -convertHistoryFile=True -historyFile=gulp.his -ncFile=gulp.nc',
                'if [ -e gulp.nc ]; then rm gulp.his; fi',
                #"""/usr/local/python-2.6.2/bin/python2.6 -c "import os; if os.path.exists('gulp.nc'): os.remove('gulp.his')" """,
                         ] 
        #foxtrot
        elif job.server.id=='server003':
            cmds = [
                '#!/usr/bin/env bash',
                'source /home/danse-vnf-admin/.vnf',
                #'. ~/.vnf',
                #'. ~/.gulp-env',
                'mpirun -np %d gulp_openmpi < %s > %s' % (np, computation.inputFile, computation.output_filename),
                '',
                ]
            if self.convertHistoryFile:
                cmds += [
                '/usr/local/python-2.6.2/bin/python2.6 /home/danse-vnf-admin/dv/tools/pythia-0.8/bin/conversionTasks.py -convertHistoryFile=True -historyFile=gulp.his -ncFile=gulp.nc',
                'if [ -e gulp.nc ]; then rm gulp.his; fi',
                #"""/usr/local/python-2.6.2/bin/python2.6 -c "import os; if os.path.exists('gulp.nc'): os.remove('gulp.his')" """,
                         ] 
                
                
        if self.serializePhononArrays:
            cmds += [
            'postProcessGulp.py -serializePhononArrays=True',
                     ] 
        if self.createPhononModesFile:
            cmds += [
            'postProcessGulp.py -historyFile=output.history -ncFile=output.nc',
                     ] 
        script = self.shscriptname
        path = self._path(script)
        open(path, 'w').write('\n'.join(cmds))
        return script
  
def job_builder(name, path):
    return Builder(name, path)


# version
__id__ = "$Id$"

# End of file 
