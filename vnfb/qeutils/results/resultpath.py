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

import os
import re
from vnfb.qeutils.qeutils import dataroot
from vnfb.qeutils.qeconst import OUTPUT_EXT, INPUT_EXT
from vnfb.qeutils.results.resultinfo import ResultInfo
#from vnfb.qeutils.qetaskinfo import TaskInfo
from vnfb.qeutils.qerecords import SimulationRecord

input_ext   = INPUT_EXT.strip(".")  # Refined input extention
output_ext  = OUTPUT_EXT.strip(".") # Refined output extention
INPUT   = '[\w]+\.%s$' % input_ext                      # Input file,  Example: "AAAAA.in"
OUTPUT  = '[\w]+\.%s\.%s$' % (input_ext, output_ext)    # Output file, Example: "AAAAA.in.out"
CRASH   = 'CRASH'                                       # Crash file

REEXP   = {}    # Dictionary of regular expressions for file types
REEXP["input"]  = INPUT
REEXP["output"] = OUTPUT
REEXP["crash"]  = CRASH


class ResultPath(object):
    def __init__(self, director, simid, type):
        self._director      = director
        self._simid         = simid     # Simulation id
        self._type          = type      # Task type
        self._init()


    def _init(self):
        "Additional initialization"
        simrecord   = SimulationRecord(director, simid)   # Have as an attribute instead?
        self._jit   = simrecord.jobInputTask(self._type)
        

    def resultFiles(self, ftype = None):
        """
        Retruns absolute path of the result file(s) specified by file type (ftype), e.g.
        output or input config files

        Example: "/home/dexity/exports/vnf/vnfb/content/data/tmp/tmpTsdw21/4ICDAVNK/4I2NPMY4pw.in.out"
        We should be able to identify input and output files without input record!
        """

        if not ftype:                # all files in the result directory
            return self._allFiles()

        files   = self.filesList()

        if not ftype in REEXP or not files:   # No entry, no file!
            return None

        file    = self._matchCheck(files, ftype)
        if file:
            # path is not None (was verified before!)
            return os.path.join(self.localPath(), file)

        return None


    def filesList(self):
        "Returns list of file names"
        path    = self.localPath()
        if not path:
            return None

        if os.path.exists(path):
            return self._filesList(path)

        return None


    def _matchCheck(self, files, ftype):
        "Find matching file. Single matching file if possible. Picks first otherwise"
        for fname in files:
            p   = re.compile(REEXP[ftype])
            if p.match(fname):   # matches
                return fname

        return None


    def _allFiles(self):
        "Returns list of *absolute* file names"
        path    = self.localPath()
        if os.path.exists(path):
            return self._files(path)

        return None


    def _files(self, path):
        "Returns list of full file names"
        files       = []
        fileslist   = self.filesList(path)
        for f in fileslist:
            files.append(os.join(path, f))

        return files


    def _filesList(self, path):
        "Filters files only and returns list of file names"
        # Example: ["4I2NPMY4pw.in", "4I2NPMY4pw.in.out", "run.sh"]
        files   = []
        entries = os.listdir(path)

        for e in entries:   # Filter files
            if os.path.isfile(os.path.join(path, e)):
                files.append(e)

        return files


    def remotePath(director, simid, type):
        """Returns the path of the jobs directory on the remote server.
        Example: /home/dexity/espresso/qejobs/5YWWTCQT/
        """
        path    = ""
        task    = qetask(director, simid, type)

        if not task:
            return path

        jobs    = director.clerk.getQEJobs(where="taskid='%s'" % task.id)
        if len(jobs) > 0:
            # Find latest job for the task
            job = latestJob(jobs)

            if job:
                server  = director.clerk.getServers(id=job.serverid)
                path    = os.path.join(server.workdir, job.name)
                path    = os.path.join(path, job.id)

        return path


    def _localPath(self):
        """
        Each job for the task of type will have separate root path specified by
        task type (ttype)

        Example: "/home/dexity/exports/vnf/vnfb/content/data/tmp/tmpTsdw21/4ICDAVNK/
        Note: Result path is assumed not to have child directories.
        """

        if not self._recordsOK():
            return None
        
        results     = ResultInfo(self._director, self._simid, self._type) 
        if results.ready():
            datadir     = dataroot(self._director)
            return os.path.join(datadir, results.tardir())

        return None     # default case


    def _recordsOK(self):
        "Checks if the proper records exist"
        if not self._jit:         # No jit, no path
            return False

        (job_, input_, task_)   = (self._jit[0], self._jit[1], self._jit[2])  # input_ not used
        if not job_ or not task_:   # If job or task is None
            return False

        return True


__date__ = "$Mar 17, 2010 9:05:14 PM$"


