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


import journal
debug = journal.debug( 'torque' )



class Scheduler:

    
    def __init__(self, launcher, prefix = None, outputstr_maxlen = 2048):
        self.prefix = prefix
        self.launcher = launcher
        self.outputstr_maxlen = outputstr_maxlen
        return
    
    
    def submit( self, cmd ):
        cmds = [ r'echo \"%s\" | qsub' % (cmd,) ]
        failed, output, error = self._launch( cmds )
        if failed:
            if error.find( 'check pbs_server daemon' ) != -1:
                from exceptions import SchedulerDaemonNotStarted
                raise SchedulerDaemonNotStarted, "pbs_server"
            msg = "error in executing cmds %s. output: %s, error: %s" % (
                cmds, output, error )
            raise RuntimeError, msg
        return output
    

    def status( self, job ):
        
        jobid = job.id_incomputingserver
        
        cmds = [ 'qstat -f %s' % (jobid,) ]
        failed, output, error  = self._launch( cmds )
        if failed:
            if error.find( 'Unknown Job Id' ) != -1:
                return self.statusByTracejob( job )
            msg = "error in executing cmds %s. output: %s, error: %s" % (
                cmds, output, error )
            raise RuntimeError, msg
        
        lines = output.split( '\n' )
        lines = lines[1:] # first line removed
        if len(lines) == 0: return self.statusByTracejob( job )
        d = {}
        for line in lines:
            try:
                k,v = line.split( '=' )
            except:
                continue
            d[ k.strip() ] = v.strip()
            continue

        errorpath = d['Error_Path']
        dummy, errorfilename = os.path.split(errorpath)

        outputpath = d['Output_Path']
        dummy, outputfilename = os.path.split(outputpath)

        state = d['job_state']
        import time
        start_time = d.get('start_time') or time.ctime()
        
        ret = {
            'remote_outputfilename': outputfilename,
            'remote_errorfilename': errorfilename,
            'status': _state( state ),
            'timeStart': start_time,
            }

        if ret['status'] == 'finished':
            output, error = self._readoutputerror(
                outputfilename, errorfilename )
            ret.update(
                { 'exit_code': d['exit_status'],
                  'timeCompletion': d['etime'],
                  'output': output,
                  'error': error,
                  } )
            pass

        return ret


    def statusByTracejob( self, job ):

        jobid = job.id_incomputingserver
        d = {}
        
        tag = 'Exit_status'
        words = self._tracejob_search( jobid, tag )
        status = words[3]
        key, value = status.split( '=' )
        assert key.lower() == 'exit_status'
        d [ 'exit_code' ] =  value

        tag = 'job was terminated'
        words = self._tracejob_search( jobid, tag )
        d[ 'timeCompletion' ] = ' '.join( words[0:2] )

        output, error = self._readoutputerror(
            job.outputfilename, job.errorfilename )

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
        cmds = [ 'tracejob %s | grep %r' % (jobid, tag) ]
        
        failed, output, error = self._launch( cmds )

        if failed:
            msg = "error in executing cmds %s. output: %s, error: %s" % (
                cmds, output, error )
            raise RuntimeError, msg

        # remove trailing \n to make parsing easier
        if output.endswith( '\n' ): output = output[:-1] 
        lines = output.split( '\n' )
        words = lines[-1].split( )
        debug.log( 'words: %s' % words )
        return words
    

    def _launch(self, cmds):
        if self.prefix: cmds = [ self.prefix ] + cmds
        return self.launcher( ' && '.join( cmds ) )

    pass # end of Scheduler

import os


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
