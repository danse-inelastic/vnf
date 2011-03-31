# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
'''
This is a wrapper of torque commands.

It is done by firing the commands and then parse the outputs.
It is not a good implementation strategy because output formats
could be changed constantly.
Better way to do this is to use python bindings of torque.
See several candidates at this moment, all without enough documentation:

http://www-unix.mcs.anl.gov/openpbs/patches/pbs_python/README.txt
https://subtrac.sara.nl/oss/pbs_python
http://code.google.com/p/py-pbs/
'''

JOBID   = "jobid"   # Filename where the job id string is stored

import journal
debug = journal.debug( 'torque' )

from pyre.units.time import hour, minute, second

class Scheduler:

    outfilename = 'STDOUT.log'
    errfilename = 'STDERR.log'
    
    def __init__(self, launcher, prefix = None, outputstr_maxlen = 2048):
        self.prefix = prefix
        self.launcher = launcher
        self.outputstr_maxlen = outputstr_maxlen
        return
    
    
    def submit( self, cmd, walltime=1*hour, jobid=1, numnodes = 1, corespernode = 1, workingDirectory='.'):
        "Submits job. Can raise exception"
        walltime = _walltime_str(walltime)

        """
        Example:
           cmds = ['echo \\"cd /home/danse-vnf-admin/vnf/qejobs/7QMQYNWX && sh run.sh\\" | qsub
                    -d /home/danse-vnf-admin/vnf/qejobs/7QMQYNWX -o STDOUT.log -e STDERR.log -V
                    -N 7QMQYNWX -l nodes=1:ppn=12 -']
        """

        # Command executed on remote cluster
        cmds = [ r'echo \"%s\" | qsub -d %s -l walltime=%s -o %s -e %s -V -N %s -l nodes=%s:ppn=%s' % (
            cmd, workingDirectory, walltime, self.outfilename, self.errfilename, jobid, numnodes, corespernode) ]

        # Actual launch of job
        failed, output, error = self._launch( cmds )
        
        if failed:
            if error.find( 'check pbs_server daemon' ) != -1:
                from exceptions import SchedulerDaemonNotStarted
                raise SchedulerDaemonNotStarted, "pbs_server"
            msg = "error in executing cmds %s. output: %s, error: %s" % (
                cmds, output, error )
            raise RuntimeError, msg
        rt =  output.strip()
        debug.log('torque job id: %s' % rt)
        return rt
    

    def delete(self, jobid):
        "Deletes job specified by jobid. Can raise exception"
        cmds = ['qdel %s' % jobid]
        failed, output, error  = self._launch( cmds )
        if failed:
            msg = "error in executing cmds %s. output: %s, error: %s" % (
                cmds, output, error )
            raise RuntimeError, msg

        return failed   # returns if job was successfully deleted
    

    def status( self, jobid ):
        "Returns job status specified by jobid. Can raise exception"
        cmds = [ 'qstat -f %s' % (jobid,) ]
        failed, output, error  = self._launch( cmds )
        if failed:
            if error.find( 'Unknown Job Id' ) != -1:
                return self.statusByTracejob( jobid )
            msg = "error in executing cmds %s. output: %s, error: %s" % (
                cmds, output, error )
            raise RuntimeError, msg
        
        lines = output.split( '\n' )
        lines = lines[1:] # first line removed
        if len(lines) == 0:
            return self.statusByTracejob( jobid )
        d = {}
        for line in lines:
            try:
                k,v = line.split( '=' )
            except:
                continue
            d[ k.strip() ] = v.strip()
            continue

        import time
        
        ret = {
            'remote_outputfilename':    self.errfilename,
            'remote_errorfilename':     self.outfilename,
            'state':                    _state( d['job_state'] ),
            'time_start':               d.get('start_time') or time.ctime()
            }

        # Right after start there is no key: resources_used.walltime
        ret['runtime']  = d.get('resources_used.walltime') or "00:00:00"


        if ret['state'] == 'finished':
            output, error = self._readoutputerror( self.outfilename, self.errfilename )
            ret.update(
                { 'exit_code':          d['exit_status'],
                  'time_completion':    d['mtime'],
                  'output':             output,
                  'error':              error,
                  } )
            pass

        return ret


    def jobId(self):
        """
        Returns job id. Tries to find file 'jobid' in that directory passed to launcher and parse job id
        """
        cmds = [ 'cat %s' % JOBID]
        failed, output, error  = self._launch( cmds )
        if failed:
            return None # No jobid found

        try:
            # output has format like: 7919.foxtrot.danse.us
            list    = output.split(".")
            jobid   = int(list[0])
        except:     # Format is different from integer
            return None

        return str(jobid)


    # XXX: Tracing job state after it is completed is very system dependent!
    def statusByTracejob( self, jobid ):
        ""
        d = {}
        
        try:
            tag = 'Exit_status'
            words = self._tracejob_search( jobid, tag )
        except self.TracejobFailed:
            # this job must have been terminated for a long time
            return self.unknownTerminatedStatus(jobid)

        status = words[3]
        key, value = status.split( '=' )
        assert key.lower() == 'exit_status'
        d [ 'exit_code' ] =  value

        try:
            tag = 'job was terminated'
            words = self._tracejob_search( jobid, tag )
        except self.TracejobFailed:
            # this job must have been terminated for a long time
            return self.unknownTerminatedStatus(jobid)

        d[ 'time_completion' ] = ' '.join( words[0:2] )

        output, error = self._readoutputerror(
            self.outfilename, self.errfilename )

        d.update( {
            'output': output,
            'error': error,
            'state': 'terminated',
            } )
            
        return d


    def unknownTerminatedStatus(self, jobid):
        d = {}
        d['exit_code'] = '999999'
        d['state'] = 'terminated'
        output, error = self._readoutputerror(
            self.outfilename, self.errfilename )

        d.update( {
            'output': output,
            'error': error,
            } )
        return d


    def _readoutputerror(self, outputfilename, errorfilename ):
        return self._read( outputfilename ), self._read( errorfilename )


    def _read(self, filename):
        'read file in the remote job directory'
        cmds = [ 'tail %r' % (filename,) ]
        failed, output, error = self._launch( cmds )
        if failed:
            msg = "error in executing cmds %s. output: %s, error: %s" % (
                cmds, output, error )
            raise RuntimeError, msg
        maxlen = self.outputstr_maxlen
        return output[-maxlen+1:]


    def _tracejob_search(self, jobid, tag):
        jobid = jobid.strip()
        cmds = [ 'tracejob %s | grep %r' % (jobid, tag) ]

        failed, output, error = self._launch( cmds )

        if failed:
            msg = "error in executing cmds %s. output: %s, error: %s" % (
                cmds, output, error )
            raise self.TracejobFailed, msg

        # remove trailing \n to make parsing easier
        if output.endswith( '\n' ): output = output[:-1] 
        lines = output.split( '\n' )
        words = lines[-1].split( )
        debug.log( 'words: %s' % words )
        return words

    class TracejobFailed(Exception): pass
    

    def _launch(self, cmds):
        if self.prefix: cmds = [ self.prefix ] + cmds
        return self.launcher( ' && '.join( cmds ) )

    pass # end of Scheduler


import os



def _walltime_str(time):
    seconds = int(time/second)%60
    seconds = '%0*d' % (2, seconds)
    
    mins = int(time/minute)%60
    mins = '%0*d' % (2, mins)
    
    hours = int(time/hour)
    hours = str(hours)
    return ':'.join([hours, mins, seconds])

_states = {
    'C': 'finished',
    'R': 'running',
    'Q': 'queued',
    'E': 'exiting', #after having run
    'H': 'onhold',
    'T': 'moved',
    'W': 'waiting',
    'S': 'suspend',
    }
    
def _state( state ):
    r = _states.get( state )
    if r: return r
    return 'unknown state: %s' % state


def test():
    import os
    s = Scheduler( os.system )
    print s.submit( 'ls' )
    return


def main():
    test()
    return


if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
