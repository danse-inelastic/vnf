import os.path
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
from vnfb.qeutils.qeresults import QEResults
from vnfb.qeutils.qetaskinfo import TaskInfo
from vnfb.qeutils.qerecords import SimulationRecord

"""
Regular expressions for various types of files
Note: 
    - id is assumed to have alphanumeric values only
    - it is assumed that there are no two files matching the same pattern!
"""
input_ext   = INPUT_EXT.strip(".")  # Refined input extention
output_ext  = OUTPUT_EXT.strip(".") # Refined output extention
INPUT   = '[\w]+\.%s$' % input_ext                      # Input file
OUTPUT  = '[\w]+\.%s\.%s$' % (input_ext, output_ext)    # Output file
CRASH   = 'CRASH'                                       # Crash file

REEXP   = {}    # Dictionary of regular expressions
REEXP["input"]  = INPUT
REEXP["output"] = OUTPUT
REEXP["crash"]  = CRASH

class QEResult(object):

    def __init__(self, director, simid, type):   # simulation id
        self._type          = type               # type name. Example: "PW"
        self._director      = director
        self._simid         = simid
        self._simrecord     = SimulationRecord(director, simid)

        # Attributes
        self._task          = None     # Will remain None if output file is not available
        self._input         = None
        self._output        = None
        self._init()


    def _init(self):
        "Retrieve output file and parse it"
        input       = self.resultFiles("input")    # Input file
        output      = self.resultFiles("output")   # Output file

        # Important line! No output file, no results!
        if not output:
            return

        self._task    = self._taskFactory(input, output)
        self._input   = self._task.input
        self._output  = self._task.output

        self._input.parse()
        self._output.parse()


    def resultPath(self):
        return self._resultPath(self._type)


    def filesList(self):
        "Returns list of file names"
        path    = self.resultPath()
        if not path:
            return None
        
        if os.path.exists(path):
            return self._filesList(path)

        return None


    def _taskFactory(self, input, output):
        "Task factory, should be subclassed"


    def resultFiles(self, type=None):
        "Retruns absolute path of the result files, e.g. output or input config files"
        # Example: "/home/dexity/exports/vnf/vnfb/content/data/tmp/tmpTsdw21/4ICDAVNK/4I2NPMY4pw.in.out"
        # We should be able to identify input and output files without input record!

        if not type:                # all files in the result directory
            return self._allFiles()

        files   = self.filesList()

        if not type in REEXP or not files:   # No entry, no file!
            return None

        file    = self._matchCheck(files, type)
        if file:
            # path is not None (it was verified before!)
            return os.path.join(self.resultPath(), file)

        return None     #

    def _matchCheck(self, files, type):
        "Find matching file. Single matching file if possible. Picks first otherwise"
        for fname in files:
            p   = re.compile(REEXP[type])
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


    def _resultPath(self, type):
        """
        Each job for the task of type will have separate root path
        Example: "/home/dexity/exports/vnf/vnfb/content/data/tmp/tmpTsdw21/4ICDAVNK/
        Note: Result path is assumed not to have child directories. 
        """
        jit     = self._simrecord.jobInputTask(type)
        if not jit:         # No jit, no path
            return None

        (_job, _input, _task)   = (jit[0], jit[1], jit[2])  # _input not used
        if not _job or not _task:   # If job or task is None
            return None

        datadir     = dataroot(self._director)
        taskinfo    = TaskInfo(simid = self._simid, type = self._type)
        results     = QEResults(self._director, _job, taskinfo)
        if results.ready():
            return os.path.join(datadir, results.tardir())

        return None     # default case


__date__ = "$Mar 17, 2010 12:21:27 PM$"


# Keep the code in case if you want to use input (which is not very smart!)
#
#            if _input and _task.type == "PW":   # PW type
#                datadir     = dataroot(self._director)
#                taskinfo    = TaskInfo(simid = self._simid, type = "PW")
#                results     = QEResults(self._director, _job, taskinfo)
#                if results.ready():
#                    file        = "%s%s" % (_input.id, defaultInputName(_task.type))
#                    if type == "output":
#                        file    += OUTPUT_EXT   # .out
#                    path        = os.path.join(results.tardir(), file)
#                    return os.path.join(datadir, path)


