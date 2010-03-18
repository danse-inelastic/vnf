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

class QEResult(object):

    def __init__(self, director, simid, type):   # simulation id
        self._type          = type               # type name. Example: "PW"
        self._director      = director
        self._simid         = simid

        # Attributes
        self._task          = None     # Will remain None if output file is not available
        self._input         = None
        self._output        = None
        self._init()


    def _init(self):
        "Retrieve output file and parse it"
        resultPath  = ResultPath(self._director, self._simid, self._type)

        input       = resultPath.resultFiles("input")    # Input file
        output      = resultPath.resultFiles("output")   # Output file

        # Important line! No output file, no results!
        if not output:
            return

        self._task    = self._taskFactory(input, output)
        self._input   = self._task.input
        self._output  = self._task.output

        self._input.parse()
        self._output.parse()
    

    def _taskFactory(self, input, output):
        "Task factory, should be subclassed"


__date__ = "$Mar 17, 2010 12:21:27 PM$"

