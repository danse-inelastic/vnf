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
        self._simrecord     = SimulationRecord(director, simid)


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
            return os.path.join(self.resultPath(), file)

        return None


    def filesList(self):
        "Returns list of file names"
        path    = self.resultPath()
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
        path    = self.resultPath()
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


    def resultPath(self):
        return self._resultPath(self._type)


    def _resultPath(self, ttype):
        """
        Each job for the task of type will have separate root path specified by
        task type (ttype)

        Example: "/home/dexity/exports/vnf/vnfb/content/data/tmp/tmpTsdw21/4ICDAVNK/
        Note: Result path is assumed not to have child directories.
        """
        jit     = self._simrecord.jobInputTask(ttype)
        if not jit:         # No jit, no path
            return None

        (_job, _input, _task)   = (jit[0], jit[1], jit[2])  # _input not used
        if not _job or not _task:   # If job or task is None
            return None

        datadir     = dataroot(self._director)
        results     = ResultInfo(self._director, self._simid, self._type) 
        if results.ready():
            return os.path.join(datadir, results.tardir())

        return None     # default case


__date__ = "$Mar 17, 2010 9:05:14 PM$"


