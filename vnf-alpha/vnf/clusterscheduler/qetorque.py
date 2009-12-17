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
from vnf.clusterscheduler.torque import _walltime_str

class Scheduler(base):

    def setSimulationParams(self, sim, settings, server):
        "Set simulation objects"
        self._sim       = sim       # not None
        self._settings  = settings  # not None
        self._server    = server    # not None
        

    def submit( self, cmd, walltime=1*hour ):
        walltime = _walltime_str(walltime)

        # Example:
        #   dir = "/home/dexity/espresso/qesimulations/MQDHXV7"
        #   str = "-V -N myjob -l nodes=8:ppn=12"
        
        dir     = "%s/%s/%s" % (self._server.workdir, self._sim.name, self._sim.id)
        str     = "-V -N %s -l nodes=%s:ppn=%s"  % (self._sim.id, self._settings.numnodes, self._server.corespernode)
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


