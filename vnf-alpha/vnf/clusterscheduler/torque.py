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
See several candidates at this moment, all without enoughh documentation:

http://www-unix.mcs.anl.gov/openpbs/patches/pbs_python/README.txt
https://subtrac.sara.nl/oss/pbs_python
http://code.google.com/p/py-pbs/
'''



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
    
    
    def submit( self, cmd, walltime=1*hour ):
        walltime = _walltime_str(walltime)
        
        cmds = [ r'echo \"%s\" | qsub -l walltime=%s -o %s -e %s' % (
            cmd, walltime, self.outfilename, self.errfilename) ]
        failed, output, error = self._launch( cmds )
        if failed:
            if error.find( 'check pbs_server daemon' ) != -1:
                from exceptions import SchedulerDaemonNotStarted
                raise SchedulerDaemonNotStarted, "pbs_server"
            msg = "error in executing cmds %s. output: %s, error: %s" % (
                cmds, output, error )
            raise RuntimeError, msg
        return output.strip()


    def delete(self, jobid):
        cmds = ['qdel %s' % jobid]
        failed, output, error  = self._launch( cmds )
        if failed:
            msg = "error in executing cmds %s. output: %s, error: %s" % (
                cmds, output, error )
            raise RuntimeError, msg
        return
    

    def status( self, jobid ):
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
        if len(lines) == 0: return self.statusByTracejob( jobid )
        d = {}
        for line in lines:
            try:
                k,v = line.split( '=' )
            except:
                continue
            d[ k.strip() ] = v.strip()
            continue

        #errorpath = d['Error_Path']
        #dummy, errorfilename = os.path.split(errorpath)
        #assert errorfilename == self.errfilename, '%r != %r' % (errorfilename, self.errfilename)
        errorfilename = self.errfilename

        #outputpath = d['Output_Path']
        #dummy, outputfilename = os.path.split(outputpath)
        #assert outputfilename == self.outfilename, '%r != %r' % (outputfilename, self.outfilename)
        outputfilename = self.outfilename

        state = d['job_state']
        import time
        start_time = d.get('start_time') or time.ctime()
        
        ret = {
            'remote_outputfilename': outputfilename,
            'remote_errorfilename': errorfilename,
            'state': _state( state ),
            'time_start': start_time,
            }

        if ret['state'] == 'finished':
            output, error = self._readoutputerror(
                outputfilename, errorfilename )
            ret.update(
                { 'exit_code': d['exit_status'],
                  'time_completion': d['mtime'],
                  'output': output,
                  'error': error,
                  } )
            pass

        return ret


    def statusByTracejob( self, jobid ):

        d = {}
        
        tag = 'Exit_status'
        try:
            words = self._tracejob_search( jobid, tag )
        except self.TracejobFailed:
            # this job must have been terminated for a long time
            return self.unknownTerminatedStatus(jobid)
            
        status = words[3]
        key, value = status.split( '=' )
        assert key.lower() == 'exit_status'
        d [ 'exit_code' ] =  value

        tag = 'job was terminated'
        words = self._tracejob_search( jobid, tag )
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
