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

    from vnf.dom.ins.VacfComputation import VacfComputation as Computation

    trajectory = 'output.history'

    def __init__(self, path):
        base.__init__(self, path)
        return

    def render(self, computation, db=None, dds=None):
        Computation = self.Computation
        
        # the job
        job = computation.job.dereference(db)
        # the server this job is going to run on
        server = job.server.dereference(db)
        
        # the gulp simulation that this computation depends on
        gulpsimulation = computation.gulpsimulation.dereference(db)
        
        # the job for the gulp simulation
        gulpjob = gulpsimulation.job.dereference(db)
        gulpserver = gulpjob.server.dereference(db)
        dds.remember(gulpjob, files = [self.trajectory], server=gulpserver)
        
        # make gulp job available on the server this job will be run
        dds.make_available(gulpjob, files = [self.trajectory], server=server)
        
        # generate the input script for pMoldyn.py
        from kernelGenerator.trajectory.PmoldynInputFileCreator import PmoldynInputFileCreator       
       
        files = []
        # add run.sh
        files.append( self._make_script(computation) )
        return files


    def _make_script(self, computation):
        job = computation.job.dereference(self.db)
        dds = self.dds
        db = self.db
        # should be replaced with
        # dds.relpath(...)
        gulpsimulation = computation.gulpsimulation.dereference(db)
        gulpjob = gulpsimulation.job.dereference(db)
        import os
        trajectory = os.path.join('..', gulpjob.id, self.trajectory)
        subs = {'units': computation.units,
                'weights': computation.weights,
                'trajectory': trajectory,
                }
        runConversionCmd = ''
        rungovcmd = 'gov.py --units=%(units)s --weights=%(weights)s --trajectory=%(trajectory)s' % subs
        
        cmds = [
            '#!/usr/bin/env sh',
            '. ~/.vacf-env',
            rungovcmd,
            ]
        script = self.shscriptname
        path = self._path(script)
        open(path, 'w').write('\n'.join(cmds))
        return script
        


# version
__id__ = "$Id$"

# End of file 
