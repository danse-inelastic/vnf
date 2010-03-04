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

# See also vnfb/applications/ITaskApp.py
# XXX Fix me!!!

#import time
#
from vnfb.dom.QEJob import QEJob
from vnfb.utils.qeutils import makedirs, writefile, stamp
from vnfb.utils.qeconst import STATES, RUNSCRIPT, TYPE, NOPARALLEL
from vnfb.utils.qeutils import packname, unpackname
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
"""

class QEDriver(base):

    class Inventory(base.Inventory):
        id          = pyre.inventory.str('id', default='')      # Simulation Id
        taskid      = pyre.inventory.str('taskid', default='')
        subtype     = pyre.inventory.str('subtype', default='')
        
        idd = pyre.inventory.facility('idd-session', factory=pyre.idd.session, args=['idd-session',])
        idd.meta['tip'] = "access to the token server"

        clerk = pyre.inventory.facility(name="clerk", factory=vnfb.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        dds = pyre.inventory.facility(name="dds", factory=vnfb.components.dds)
        dds.meta['tip'] = "the component manages data files"

        csaccessor = pyre.inventory.facility(name='csaccessor', factory = vnfb.components.ssher)
        csaccessor.meta['tip'] = 'computing server accessor'


    def main(self):
        open("/tmp/qedriver.txt", "w").write("Hello")
#        sim = self.clerk.getQESimulations(id = self.id)
#        sim.setClerk(self.clerk)
#        sim.updateRecord({"label": "Hi",})

#        self.submitJob()


#    def submitJob(self):
#        """
#        Submit simulation job
#        The process of submission of simulation includes the following steps:
#        1. Store configuration inputs to local disk storage
#        2. Copy files to the computational cluster
#        3. Submit Job
#        """

#        self._createJob()
#        self._storeFiles()
#        self._moveFiles()
#        self._scheduleJob()


#    def _createJob(self):
#        "Create Job"
        
#        sim = self.clerk.getQESimulations(id = self.id)
#        self._sim   = self.clerk.getQESimulations(id = self.id)     # Should exist
#        settings    = self.clerk.getQESettings(where = "simulationid='%s'" % self.id)   # Should exist
#        setting     = settings[0]
#        params  = {"taskid":        self.taskid,
#                   "serverid":      self._sim.serverid,  # -> take from QESimulations
#                   "status":        "Submitted",    # Fixed status
#                   "timesubmitted": stamp(),
#                   "creator":       self.sentry.username,
#                   "numberprocessors":   setting.numproc, # -> take from QESettings
#                   "description":   self.subtype
#                   }

#        debug   = False  # Debugging flag
#        if debug:
#            #self.taskid = "4FUNHMTP"
#            self.taskid = "46M3E9PE"
#            jobs        = self.clerk.getQEJobs(where = "taskid='%s'" % self.taskid) # Temp
#            self._job   = jobs[0]
#        else:

#        self._job  = QEJob()
#        self._job.setDirector(self)
#        #self._job.createRecord(params)


#    def _storeFiles(self):
#        """TEMP SOLUTION: Stores files from configuration input strings """
#        self._storeConfigurations()
#        self._createRunScript()
#        self._prepareFiles()
#
#
#    def _storeConfigurations(self):
#        "Store Configuration files"
#        inputs  = self.clerk.getQEConfigurations(where = "taskid='%s'" % self.taskid)
#        dds     = self.dds
#        for input in inputs:
#            fn          = input.filename
#            pfn         = packname(input.id, fn)                # E.g. 44XXJJG2ni.scf.in
#            self._write2file(dds, input, fn, input.text)        # -> qeconfigurations directory
#            self._write2file(dds, self._job, pfn, input.text)   # -> qejobs directory
#            dds.remember(self._job, pfn)     # Change object and filename?
#            self._files.append(pfn)
#
#
#    def _createRunScript(self):
#        settingslist = self.clerk.getQESettings(where = "simulationid='%s'" % self.id)       # not None
#        inputs      = self.clerk.getQEConfigurations(where = "taskid='%s'" % self.taskid)
#        task        = self.clerk.getQETasks(id = self.taskid)
#        server      = self.clerk.getServers(id = self._job.serverid)
#        settings    = settingslist[0]
#        input       = inputs[0]
#
#        # mpirun --mca btl openib,sm,self pw.x -npool 8 -inp  PW > PW.out
#        words   = [ settings.executable,
#                    settings.params,
#                    TYPE[task.type],
#                    "-npool %s" % self._npool(settings, task.type),
#                    "-inp",
#                    packname(input.id, input.filename),       # replace
#                    ">",
#                    packname(input.id, "%s.out" % input.filename)    # replace
#        ]
#
#        # QE temp simulation directory is qesimulations/[simid] directory
#        # E.g.: /home/dexity/espresso/qesimulations/3YEQ8PNV    -> no trailing slash
#        qetempdir  = self.dds.abspath(self._sim, server=server)
#        cmds    = [ "#!/bin/env bash",   # Suppose there is bash available
#                    "export ESPRESSO_TMPDIR=%s/" % qetempdir,
#                    " ".join(words)
#        ]
#
#        dds     = self.dds
#        self._write2file(dds, self._job, RUNSCRIPT, "\n".join(cmds))    # -> qejobs directory
#        dds.remember(self._job, RUNSCRIPT)  # Important step during which the .__dds_nodelist* files are created
#        self._files.append(RUNSCRIPT)
#
#
#    def _npool(self, settings, type):
#        "Returns npool depending on type of simulation task"
#        # suppose settings is not None
#        num = settings.npool
#        if type in NOPARALLEL:
#            num = 1
#
#        return num
#
#
#
#    def _write2file(self, dds, record, fname, content):
#        """Writes content of the configuration input to file"""
#        path        = dds.abspath(record)
#        absfilename = dds.abspath(record, filename = fname)
#        makedirs(path)
#        writefile(absfilename, content)
#
#
#    def _moveFiles(self):
#        """
#        Moves files from local server to the computational cluster.
#        Files that need to be moved:
#            - Configuration inputs
#            - Simulation Settings
#            - run.sh script (generate it first)
#        Notes:
#            - See also: submitjob.odb
#        """
#        dds     = self.dds
#        server  = self.clerk.getServers(id = self._job.serverid)
#        dds.make_available(self._job, server=server, files=self._files)
#
#        # Create output directory (ESPRESSO_TEMPDIR) for QE
#        dds.makedirs(self._sim, server=server)
#
#
#    def _test_makedirs(self):
#        dds         = self.dds
#        self._sim   = self.clerk.getQESimulations(id = self.id)
#        server      = self.clerk.getServers(id = self._sim.serverid)
#        dds.makedirs(self._sim, server=server)
#
#
#    def _scheduleJob(self):
#        "Schedule job"
#        dds     = self.dds
#        from vnfb.utils.qescheduler import schedule
#        schedule(self._sim, self, self._job)


    def __init__(self):
        super(QEDriver, self).__init__( 'qedriver')


    def _configure(self):
        super(QEDriver, self)._configure()
        self.id         = self.inventory.id
        self.taskid     = self.inventory.taskid
        self.subtype    = self.inventory.subtype

        self.idd        = self.inventory.idd
        self.clerk      = self.inventory.clerk
        self.dds        = self.inventory.dds
        self.csaccessor = self.inventory.csaccessor
        self.clerk.director     = self
        self.dds.director       = self


    def _init(self):
        super(QEDriver, self)._init()


__date__ = "$Mar 3, 2010 11:04:10 PM$"


#        sim = self.clerk.getQESimulations(id = self.id)
#        sim.setClerk(self.clerk)
#        sim.updateRecord({"label": "Hi",})



