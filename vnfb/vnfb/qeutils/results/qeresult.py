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
from vnfb.qeutils.results.resultpath import ResultPath

"""
Regular expressions for various types of files
Note: 
    - id is assumed to have alphanumeric values only
    - assumed that there are no two files matching the same pattern!
"""

# XXX: Handle the case when the results files might not have read access
class QEResult(object):

    def __init__(self, director, simid, linkorder):   # simulation idtype, 
        self._director      = director
        self._simid         = simid
        self._linkorder     = linkorder
        self._resultPath    = ResultPath(director, simid, linkorder)

        # Attributes
        self._task          = None  # None if output file is not available or task factory not implemented
        self._input         = None
        self._output        = None
        self._init()


    def _init(self):
        "Retrieve output file and parse it"
        self._inputFile     = self._resultPath.resultFiles("input")    # Input file
        self._outputFile    = self._resultPath.resultFiles("output")   # Output file
        self._localPath     = self._resultPath.localPath()    # Local results directory
        self._remotePath    = self._resultPath.remotePath()   # Remote results directory

        # Important line! No output file, no results!
        if not self._outputFile:
            return

        self._task    = self._taskFactory()

        # Sometimes I don't need task object and don't implement task factory
        if not self._task:      
            return

        self._input   = self._task.input
        self._output  = self._task.output

        self._input.parse()
        self._output.parse()
    

    def localPath(self):
        "Local results directory"
        return self._localPath


    def remotePath(self):
        "Remote results directory"
        return self._remotePath


    def input(self):
        "Returns input object (subclass of QEInput)"
        return self._input


    def output(self):
        "Returns output object (subclass of QEInput)"
        return self._output


    def resultPath(self):
        "Returns object of ResultPath class"
        return self._resultPath


    def setLinkOrder(self, linkorder):
        "Sets link order"
        self._linkorder   = linkorder


    def _taskFactory(self):
        "Task factory, should be subclassed"


__date__ = "$Mar 17, 2010 12:21:27 PM$"

