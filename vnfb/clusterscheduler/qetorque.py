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
debug = journal.debug( 'qetorque' )

from pyre.units.time import hour, minute, second
import math

from vnfb.clusterscheduler.torque import Scheduler as base
from vnfb.clusterscheduler.torque import _walltime_str
from vnfb.qeutils.qeconst import NOPARALLEL

PROC_PER_NODE   = 12    # Number of processors per node, specific for foxtrot

class Scheduler(base):

    def setSimulationParams(self, job, settings, server, task):
        "Set simulation objects"
        self._job       = job       # not None
        self._settings  = settings  # not None
        self._server    = server    # not None
        self._task      = task      # not None


    def submit( self, cmd, walltime=1*hour ):
        walltime = _walltime_str(walltime)

        """
        Example:
           dir  = "/home/dexity/espresso/qesimulations/MQDHXV7"
           str  = "-V -N myjob -l nodes=8:ppn=12"
           cmds = ['echo \\"cd /home/dexity/espresso/qejobs/7QMQYNWX && sh run.sh\\" | qsub
                    -d /home/dexity/espresso/qejobs/7QMQYNWX -o STDOUT.log -e STDERR.log -V
                    -N 7QMQYNWX -l nodes=1:ppn=12 -']
        """

        dir     = "%s/%s/%s" % (self._server.workdir, self._job.name, self._job.id)
        str     = "-V -N %s -l nodes=%s:ppn=%s"  % (self._job.id, self._nodes(), self._ppn())
        str     = str + " -l walltime=%s" % walltime    # Add walltime
        # Command executed on remote cluster
        cmds    = [ r'echo \"%s\" | qsub -d %s -o %s -e %s %s -' % (
            cmd, dir, self.outfilename, self.errfilename, str) ]

        # Actual launch of job
        failed, output, error = self._launch( cmds )

        if failed:
            if error.find( 'check pbs_server daemon' ) != -1:
                from exceptions import SchedulerDaemonNotStarted
                raise SchedulerDaemonNotStarted, "pbs_server"
            msg = "error in executing cmds %s. output: %s, error: %s" % (
                cmds, output, error )
            raise RuntimeError, msg
        return output.strip()


    def _nodes(self):
        "Returns number of nodes"
        n  = self._getnodes()   
        if self._task.type in NOPARALLEL:
            n  = 1

        return n


    def _getnodes(self):
        "Calculates number of nodes (nodes) from number of processors"
        numproc = self._settings.numproc
        return int(math.ceil(numproc/float(PROC_PER_NODE)))


    def _ppn(self):
        "Returns number of processors per node"
        ppn = self._getppn()   
        if self._task.type in NOPARALLEL:
            ppn  = 1

        return ppn


    def _getppn(self):
        "Calculates number of processors per node (ppn) from number of processors"
        numproc = self._settings.numproc
        if numproc <= PROC_PER_NODE:
            return numproc

        return PROC_PER_NODE


__date__ = "$Dec 7, 2009 10:37:25 AM$"


