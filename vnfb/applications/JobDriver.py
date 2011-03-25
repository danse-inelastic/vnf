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

# Borrowed from TRGenerator class
TRAJSCRIPT  = "qe2dos.py"
VELFILE     = "cp.vel"
POSFILE     = "cp.pos"
NCFILE      = "cp.nc"
DOSFILE     = "vdos.dos"

from vnfb.dom.QEJob import QEJob
from vnfb.qeutils.results.cpresult import CPResult
from vnfb.qeutils.qeutils import stamp, writeRecordFile, defaultInputName, readRecordFile
from vnfb.qeutils.qeconst import RUNSCRIPT, TYPE, MDSTEPS, NOPARALLEL
from vnfb.qeutils.qeutils import packname
from vnfb.qeutils.qescheduler import schedule
from vnfb.qeutils.servers import outdir, createOutdir
from luban.applications.UIApp import UIApp as base

import pyre.idd
import pyre.inventory
import vnfb.components

"""
Jobs submission steps:
    - Creating job records          - 10%
    - Preparing configuration files - 20%
    - Preparing control files       - 40%
    - Copying files to cluster      - 60%
    - Submitting to queue           - 80%
    - Done                          - 100%

Important Notes:
    - Depending on cluster "<" control character on command line might not be recognized
     (see _createRunScript() method) in this case try to use "-inp".
    - Dynmat task IS NOT a parallel program (no mpirun)
    - Both "<" and "-inp" work on foxtrot.danse.us
    - See also vnfb/applications/ITaskApp.py
    - This application is specific for Quantum Espress. To use it for other package,
      you need to subclass it
"""

class JobDriver(base):

    class Inventory(base.Inventory):
        id          = pyre.inventory.str('id', default='')      # Simulation Id
        taskid      = pyre.inventory.str('taskid', default='')
        subtype     = pyre.inventory.str('subtype', default='')
        optlevel    = pyre.inventory.str('optlevel', default="0")
        
        idd = pyre.inventory.facility('idd-session', factory=pyre.idd.session, args=['idd-session',])
        idd.meta['tip'] = "access to the token server"

        clerk = pyre.inventory.facility(name="clerk", factory=vnfb.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        dds = pyre.inventory.facility(name="dds", factory=vnfb.components.dds)
        dds.meta['tip'] = "the component manages data files"

        csaccessor = pyre.inventory.facility(name='csaccessor', factory = vnfb.components.ssher)
        csaccessor.meta['tip'] = 'computing server accessor'


    def main(self):
        "Main method"
        self.submitJob()


    def submitJob(self):
        """
        Submit simulation job
        The process of submission of simulation includes the following steps:
        1. Store configuration inputs to local disk storage
        2. Copy files to the computational cluster
        3. Submit Job
        """

        self._createJob()
        self._storeFiles()
        self._moveFiles()
        self._scheduleJob()
        self._updateStatus("submitted")


    def _createJob(self):
        "Create Job"       
        self._sim   = self.clerk.getQESimulations(id = self.id)     # Should exist
        settings    = self.clerk.getQESettings(where = "simulationid='%s'" % self.id)   # Should exist
        setting     = settings[0]
        params  = {"taskid":        self.taskid,
                   "serverid":      setting.serverid,
                   "status":        "Submitting",    # Fixed status
                   "timesubmitted": stamp(),
                   "creator":       self.sentry.username,
                   "numberprocessors":   setting.numproc, # -> take from QESettings
                   "description":   self.subtype
                   }

        self._job  = QEJob(self)
        self._job.createRecord(params)
        self._updateStatus("create-job")    # Should go after job creation
        

    def _storeFiles(self):
        """TEMP SOLUTION: Stores files from configuration input strings """
        self._storeConfigurations()
        self._createRunScript()
        self._storeExtraFiles()     # Useful for trajectories


    def _storeConfigurations(self):
        "Store Configuration files"
        self._updateStatus("prepare-configs")

        inputs  = self.clerk.getQEConfigurations(where = "taskid='%s'" % self.taskid)
        dds     = self.dds

        if len(inputs) <= 0:
            return

        input   = inputs[0]     # Take the first input record

        fn          = defaultInputName(input.type)
        pfn         = packname(input.id, fn)        # E.g. 44XXJJG2pw.in

        # Read text and store it in different location.
        # Not very efficient but will work for file of size < 1Mb

        text        = readRecordFile(dds, input, fn)
        writeRecordFile(dds, self._job, pfn, text)   # -> qejobs directory
        dds.remember(self._job, pfn)     # Change object and filename?
        self._files.append(pfn)


    def _createRunScript(self):
        "Creates run script"
        self._updateStatus("prepare-controls")

        server      = self.clerk.getServers(id = self._job.serverid)
        self._task  = self.clerk.getQETasks(id = self.taskid)
        if self._task.type  == "trajectory":    # Special case for trajectory task
            args        = self._trajectoryArgs()
        else:
            args        = self._commandArgs()
        
        cmds    = [ "#!/bin/env bash",   # Suppose there is bash available
                    "export ESPRESSO_TMPDIR=%s/" % self._outdir(server),
                    " ".join(args)
        ]

        writeRecordFile(self.dds, self._job, RUNSCRIPT, "\n".join(cmds))    # -> qejobs directory
        self.dds.remember(self._job, RUNSCRIPT)  # Important step during which the .__dds_nodelist* files are created
        self._files.append(RUNSCRIPT)


    # XXX: Fix?
    def _storeExtraFiles(self):
        "Store some other files. Useful for trajectory task"
        if self._task.type  != "trajectory":  # Special case for trajectory task
            return

        self._setResultOutput()
        self._storeVelFile()
        self._storePosFile()


    def _setResultOutput(self):
        "Sets results output"
        trajLO          = self._task.linkorder  # Trajectory linkorder
        resLO           = int(trajLO) - 1       # Result linkorder
        assert resLO >= 0   # Should not be negative!
        result          = CPResult(self, self.id, linkorder = resLO)
        self._output    = result.output()
        self._step      = self._output.property('trajectory')['step']
        self._time      = self._output.property('trajectory')['time']
        self._vel       = self._output.property('trajectory')['vel']
        self._pos       = self._output.property('trajectory')['pos']


    def _storeVelFile(self):
        "Stores velocities to cp.vel file"
        str     = ""
        for ts in range(len(self._vel)):
            str += "     %s  %s\n" % (self._step[ts], self._time[ts])
            for atom in self._vel[ts]:
                str   += " %s %s %s\n" % (atom[0], atom[1], atom[2])

        str = str.rstrip("\n")
        writeRecordFile(self.dds, self._job, VELFILE, str)   
        self.dds.remember(self._job, VELFILE)  # Important step 
        self._files.append(VELFILE)


    def _storePosFile(self):
        "Stores positions to cp.pos file"
        str     = ""
        for ts in range(len(self._pos)):
            str += "     %s  %s\n" % (self._step[ts], self._time[ts])
            for atom in self._pos[ts]:
                str   += " %s %s %s\n" % (atom[0], atom[1], atom[2])

        str = str.rstrip("\n")
        writeRecordFile(self.dds, self._job, POSFILE, str)
        self.dds.remember(self._job, POSFILE)  # Important step 
        self._files.append(POSFILE)


    def _commandArgs(self):
        "Returns list of command arguments (will be later on concatenated)"
        settingslist = self.clerk.getQESettings(where = "simulationid='%s'" % self.id)       # not None
        settings    = settingslist[0]
        inputs      = self.clerk.getQEConfigurations(where = "taskid='%s'" % self.taskid)
        input       = inputs[0]

        fn          = defaultInputName(input.type)
        inputFile   = packname(input.id, fn)        # E.g. 44XXJJG2pw.in
        outputFile  = inputFile + ".out"

        # No "mpirun" for single core simulations
        if input.type in NOPARALLEL:      
            args    = [ self._qeExec(self._task.type),
                        "<",
                        inputFile,
                        ">",
                        outputFile
                        ]
            return args

        # Example: mpirun --mca btl openib,sm,self pw.x -npool 8 -inp  PW > PW.out
        args   = [ settings.executable,
                    settings.params,
                    self._qeExec(self._task.type),
                    "-npool %s" % self._npool(settings, self._task.type),
                    "-inp",        # Options: "-inp" or "<"
                    inputFile,
                    ">",
                    outputFile
                    ]

        return args


    def _trajectoryArgs(self):
        "Arguments for trajectory analysis"
        args    = [TRAJSCRIPT, ]
        return args


    def _qeExec(self, type):
        if type in TYPE.keys():
            return TYPE[type]

        if type in MDSTEPS.keys():  # Molecular dynamics
            return TYPE["CP"]

        return ""


    def _npool(self, settings, type):
        "Returns npool"
        # suppose settings is not None
        return settings.npool


    def _moveFiles(self):
        """
        Moves files from local server to the computational cluster (normally, head node).
        Files that need to be moved:
            - Configuration inputs
            - Simulation Settings
            - run.sh script (generate it first)
        Notes:
            - See also: submitjob.odb
        """
        self._updateStatus("copy-files")
        
        server  = self.clerk.getServers(id = self._job.serverid)
        self.dds.make_available(self._job, server=server, files=self._files) # NFS

        self._createOutdir(server)
       

    def _scheduleJob(self):
        "Schedule job"
        self._updateStatus("enqueue")

        schedule(self._sim, self, self._job)


    def _outdir(self, server):
        """
        Retruns output directory for QE: ESPRESSO_TEMPDIR

        QE temp simulation directory is qesimulations/[simid] directory
        E.g.: /home/dexity/espresso/qesimulations/3YEQ8PNV    -> no trailing slash
        """    
        return outdir(self, self._sim, server, self.optlevel)


    def _createOutdir(self, server):
        "Create output directory for QE: ESPRESSO_TEMPDIR"
        createOutdir(self, self._sim, server, self.optlevel) # (foxtrot: shell="bpsh -a", octopod: shell="")
        

    def _updateStatus(self, status):
        "Update job status"
        self._job.updateRecord({"status": status})


    def __init__(self):
        super(JobDriver, self).__init__( 'jobdriver')


    def _configure(self):
        super(JobDriver, self)._configure()
        self.id         = self.inventory.id
        self.taskid     = self.inventory.taskid
        self.subtype    = self.inventory.subtype
        self.optlevel   = self.inventory.optlevel

        self.idd        = self.inventory.idd
        self.clerk      = self.inventory.clerk
        self.dds        = self.inventory.dds
        self.csaccessor = self.inventory.csaccessor
        self.clerk.director     = self
        self.dds.director       = self
        


    def _init(self):
        super(JobDriver, self)._init()
        self._files = []

__date__ = "$Mar 3, 2010 11:04:10 PM$"



