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

"""
Displays the status of the job
"""
import os.path
import os
import re
from vnfb.qeutils.qeconst import ID_OUTPUT, ID_STATUS
from vnfb.qeutils.qeutils import key2str, dataroot, jobStatus, makedirs, qedialog
from vnfb.qeutils.qerecords import SimulationRecord

import luban.content as lc
from luban.content import load, select

NONE    = "None"
DEFAULT_MESSAGE = "Not Started"

class JobStatus(object):

    def __init__(self, director, simid, linkorder, job = None, outputfile=None):
        self._director  = director
        self._simid     = simid
        self._linkorder = linkorder
        self._job       = job       # specified job
        self._task      = None
        self._input     = None
        self._server    = None
        self._outputfile    = outputfile    # Output file to look into for job output

        self._init()


    def _init(self):
        simrecord       = SimulationRecord(self._director, self._simid)
        self._input     = simrecord.input(self._linkorder)
        self._task      = simrecord.task(self._linkorder)

#        if not self._job and not self._job:
#            return

        if not self._job:   # If no job is set take from simrecord
            self._job   = simrecord.job(self._linkorder)

        if not self._job:   # Job is None
            return

        self._job.setDirector(self._director)
        self._server    = self._director.clerk.getServers(id = self._job.serverid)


    def status(self, formatted=True):
        "Returns status message"
        if not formatted:   # Return just status
            return self._jobStatus()

        doc     = lc.document(id = self._statusId())
        content = lc.htmldocument(text = DEFAULT_MESSAGE)
        doc.add(content)

        if not self._job:
            return doc
        
        content.text    = key2str(self._jobStatus())
        return doc


    def updatedStatus(self):
        "Returns updated status"        
        status  = jobStatus(self._director, self._job, self._server)

        if not status:
            return "Unknown"

        if status["state"] == "terminated":
            state   = "Finished"
            self._updateJobStatus(state)
            return state

        str     = key2str(status["state"])
        if status.has_key("runtime") and status["state"] == "running":
            str     += " (%s) " % status["runtime"]

        self._updateJobStatus(str)
        return str


    def action(self):
        "Return action link"
        return self._action("refreshStatusOutput")


    def actionStatus(self):
        "Return status action"
        return self._action("refreshStatus")


    def _action(self, routine):
        "General action that calls specific routine"
        if not self._job or not self._task:
            return ""

        return lc.link(label    ="Refresh",
                      Class     = "qe-task-action",
                      onclick   = load(actor     = 'jobs/status',
                                       routine   = routine,
                                       id        = self._simid,
                                       taskid    = self._task.id,
                                       jobid     = self._job.id,
                                       linkorder = self._linkorder)
                     )

    def id(self):
        "Returns job's id"
        if not self._job:
            return None
        return self._job.id


    def output(self):
        "Returns formatted link to output file on local server"
        doc     = lc.document(id = self._outputId())
        content = lc.document()
        doc.add(content)

        outputfile  = self._outputFile()   # Output file    # self._director, self._job

        if not outputfile:    # No output file
            content.add(NONE)
            return doc

        content.add(self._fileLink(outputfile, content))
        return doc


    def updatedOutput(self, content):
        """
        Returns output file retrieved from remote cluster
        content: widget to which output is attached (needed for dialog)
        """
        if not self._job:     # No job, no output
            return NONE

        outputfile  = self._retrieveFile()

        if not outputfile:  # No file on local server
            return NONE

        return self._fileLink(outputfile, content)


    def _retrieveFile(self):
        """
        Retrieves file from remote to local server and returns filename if file 
        exists on localserver
        """
        if not self._job or not self._server:
            return None
        
        remotepath  = self._director.dds.abspath(self._job, server=self._server)
        localpath   = self._localPath()
        cmd         = "ls %s" % remotepath  # list current job directory

        failed, output, error = self._director.csaccessor.execute(cmd,
                                                                  self._server,
                                                                  remotepath,
                                                                  suppressException = True)
        if failed or not localpath:      # Something went wrong
            return None

        # List of files, Example: ["4I2NPMY4pw.in", "4I2NPMY4pw.in.out", "run.sh", ...]
        filelist    = output.split()    
        file        = self._matchCheck(filelist)

        if not file:    # No output file is found in the directory
            return None

        try:
            remotefile  = os.path.join(remotepath, file)   # File on remote server
            self._director.csaccessor.getfile(self._server, remotefile, localpath)
        except:
            return None

        filename    = os.path.join(localpath, file)
        if os.path.exists(filename):    # If file exists
            return filename

        return None


    def _fileLink(self, filename, content):
        "Returns file link"
        assert filename != None
        # Contruct dialog
        title   = 'Output for %s task. %s bytes' % (self._task.id, os.path.getsize(filename))
        text    = lc.htmldocument(text="<pre>%s<pre>" % open(filename).read())
        dialog  = qedialog(title, text) # dialog to pop up

        return lc.link(label     = 'Output',
                       onclick   = select(element=content).append(dialog))


    def _jobStatus(self):
        "Returns job status"
        if not self._job:
            return None

        return self._job.status


    def _updateJobStatus(self, str):
        "Updates job status"    # What is job is None?
        self._job.updateRecord({"status": str,})


    def _localPath(self):
        """
        Returns path to where the file will be transferred, create directory,
        if necessary
        Notes:
            The reason to copy output file to tmp/ directory is that tmp/ is
            the only one that exposed for public (linked to html directory)
        """
        if not self._job:     # No job, no output
            return None

        tmpbase     = os.path.join(dataroot(self._director, relative=True), "tmp") # Example: ../content/data/tmp
        localpath   = os.path.join(tmpbase, self._job.name)   # ../content/data/tmp/qejobs
        localpath   = os.path.join(localpath, self._job.id)     # ../content/data/tmp/qejobs/EXSWTYTK
        if not os.path.exists(localpath): # create directory, if necessary
            makedirs(localpath)     # XXX: Can through the exception

        return localpath  # Example: ../content/data/tmp/qejobs/EXSWTYTK


    def _outputFile(self):
        "Returns otuput file"
        localpath = self._localPath()

        if not localpath:
            return None

        files       = os.listdir(localpath)
        file        = self._matchCheck(files)
        if not file:    # No file,
            return None

        filename    = os.path.join(localpath, file)
        
        if os.path.exists(filename):    # Check filename again
            return filename     # Example: ../content/data/tmp/qejobs/EXSWTYTK/EYWKUYI3q2r.in.out

        return None


    # Borrowed from ResultPath class
    # XXX: Fix cardcoded pattern for output file
    def _matchCheck(self, files):
        "Find matching file. Single matching file if possible. Picks first otherwise"
        REEXP   = '[\w]+\.in\.out$' # Default regular expression for output file

        if self._outputfile:        # If output file is specified, get it
            REEXP   = self._outputfile

        for fname in files:
            p   = re.compile(REEXP)
            if p.match(fname):   # matches
                return fname

        return None

    def _statusId(self):
        if not self._job:
            return ""

        return "%s-%s" % (ID_STATUS, self._job.id)


    def _outputId(self):
        if not self._job:
            return ""
        
        return "%s-%s" % (ID_OUTPUT, self._job.id)


__date__ = "$Mar 18, 2010 11:05:41 PM$"

