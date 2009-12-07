#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

# Stub

import journal
debug = journal.debug( 'torque' )

from pyre.units.time import hour, minute, second

from vnf.clusterscheduler.torque import Scheduler as base

class Scheduler(base):
    
    def submit( self, cmd, walltime=1*hour ):
        walltime = _walltime_str(walltime)

        dir     = "/home/dexity/espresso/qeconfigurations/MQDHXV7"
        str     = "-V -N myjob -l nodes=8:ppn=12"
        cmds    = [ r'echo \"%s\" | qsub -d %s -o %s -e %s %s -' % (
            cmd, dir, self.outfilename, self.errfilename, str) ]

        failed, output, error = self._launch( cmds )
        if failed:
            if error.find( 'check pbs_server daemon' ) != -1:
                from exceptions import SchedulerDaemonNotStarted
                raise SchedulerDaemonNotStarted, "pbs_server"
            msg = "error in executing cmds %s. output: %s, error: %s" % (
                cmds, output, error )
            raise RuntimeError, msg
        return output.strip()


__date__ = "$Dec 7, 2009 10:37:25 AM$"


