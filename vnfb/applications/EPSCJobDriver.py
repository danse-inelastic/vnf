# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
from vnfb.qeutils.qeutils import stamp, writeRecordFile, latestInput, readRecordFile
from vnfb.qeutils.qeconst import RUNSCRIPT
from vnfb.qeutils.qeutils import packname
from vnfb.qeutils.qescheduler import schedule
from vnfb.qeutils.servers import outdir, createOutdir
from vnfb.epscutils.epscconst import FILETYPE, EPSC_BIN, EPSC_IN, EPSC_IN_TEXT, EPSC_OUT

from vnfb.applications.JobDriver import JobDriver as base

class EPSCJobDriver(base):

    def _storeConfigurations(self):
        "Store Configuration files"
        self._updateStatus("prepare-configs")
        #pfnlist = []

        # Save 4 config files
        for type in FILETYPE:
            inputs  = self.clerk.getQEConfigurations(where = "taskid='%s' and type='%s'" % \
                                                     (self.taskid, type))
            if len(inputs) == 0:
                return

            # assert input.type == type
            input   = latestInput(inputs)
            fn      = input.type                
            #pfn     = packname(input.id, fn)    # E.g. 44XXJJG2filecrys
            #pfnlist.append(pfn)

            # Read text and store it in different location.
            # Not very efficient but will work for file of size < 1Mb
            text    = readRecordFile(self.dds, input, fn)
            writeRecordFile(self.dds, self._job, fn, text)   # -> qejobs directory
            self.dds.remember(self._job, fn)     # Change object and filename?
            self._files.append(fn)

        # Main config file
        text    = EPSC_IN_TEXT #% pfnlist       # Should be 4 element list
        writeRecordFile(self.dds, self._job, EPSC_IN, text)   # -> qejobs directory
        self.dds.remember(self._job, EPSC_IN)     # Change object and filename?
        self._files.append(EPSC_IN)
        

    def _createRunScript(self):
        "Creates run script"
        self._updateStatus("prepare-controls")

        server      = self.clerk.getServers(id = self._job.serverid)
        self._task  = self.clerk.getQETasks(id = self.taskid)
        dest        = self.dds.abspath(self._job, server=server)    # Important

        # This is a nasty HACK!
        # EPSC simulation if NOT ever intended for usage other than on desktop!
        cmds    = [ "#!/bin/env bash",   # Suppose there is bash available
                    "",
                    "dest='%s'" % dest,       # Destination directory in qejobs (on computational cluster)
                    "",
                    "epsc3path=`which %s`" % EPSC_BIN,
                    "cp $epsc3path $dest",  # Copy binary to destination directory
                    "cd $dest",             # Go to this directory
                    "./%s > %s" % (EPSC_BIN, EPSC_OUT)] # Execute binary

        writeRecordFile(self.dds, self._job, RUNSCRIPT, "\n".join(cmds))    # -> qejobs directory
        self.dds.remember(self._job, RUNSCRIPT)  # Important step during which the .__dds_nodelist* files are created
        self._files.append(RUNSCRIPT)


__date__ = "$Mar 24, 2011 6:26:29 PM$"


