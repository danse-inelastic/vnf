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
from vnfb.utils.qeconst import NOPARALLEL

class Scheduler(base):

    def setSimulationParams(self, job, settings, server, task):
        "Set simulation objects"
        self._job       = job       # not None
        self._settings  = settings  # not None
        self._server    = server    # not None
        self._task      = task      # not None


    def submit( self, cmd, walltime=1*hour ):
        walltime = _walltime_str(walltime)

        # Example:
        #   dir = "/home/dexity/espresso/qesimulations/MQDHXV7"
        #   str = "-V -N myjob -l nodes=8:ppn=12"
        
        dir     = "%s/%s/%s" % (self._server.workdir, self._job.name, self._job.id)
        str     = "-V -N %s -l nodes=%s:ppn=%s"  % (self._job.id, self._numnodes(), self._corespernode())
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


    def _numnodes(self):
        "Returns number of nodes"
        nn  = self._settings.numnodes
        if self._task.type in NOPARALLEL:
            nn  = 1

        return nn


    def _corespernode(self):
        "Returns number of cores per node"
        cpn = self._server.corespernode
        if self._task.type in NOPARALLEL:
            cpn  = 1

        return cpn

__date__ = "$Dec 7, 2009 10:37:25 AM$"


