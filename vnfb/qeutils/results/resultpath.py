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
#from vnfb.qeutils.qerecords import SimulationRecord

def ending(ext):
    return '[\w]+\.%s$' % ext

# Extensions
DOS_EXT     = "dos"
FLVEC_EXT   = "modes"
FLFRQ_EXT   = "freq"
FLDOS_EXT   = "dos"     # aliase to DOS_EXT
input_ext   = INPUT_EXT.strip(".")  # Refined input extention
output_ext  = OUTPUT_EXT.strip(".") # Refined output extention

# Regular expressions
INPUT       = ending(input_ext)                      # Input file,  Example: "AAAAA.in"
OUTPUT      = ending(input_ext + "\." + output_ext)    # Output file, Example: "AAAAA.in.out"
CRASH       = 'CRASH'                                       # Crash file
DOS         = ending(DOS_EXT)   # Valid both for phonons and electrons
FLVEC       = ending(FLVEC_EXT)
FLFRQ       = ending(FLFRQ_EXT)
FLDOS       = ending(FLDOS_EXT)
FILOUT      = "dynmat.out"      # dynmat file with friequencies
FILBAND     = "bands.dat"
PSBAND      = "bands.ps"        # .ps file from plotband.x results
PNGBAND     = "bands.png"       # .png file converted from bands.ps
XMGRBAND    = "bands.xmgr"

# Dictionary of regular expressions for file types
REEXP   = {}    
REEXP["input"]          = INPUT
REEXP["output"]         = OUTPUT
REEXP["crash"]          = CRASH
REEXP["dos"]            = DOS     # Examples: matdyn.dos, pwscf.dos
REEXP["flvec"]          = FLVEC
REEXP["flfrq"]          = FLFRQ
REEXP["fldos"]          = FLDOS   # Aliase to "dos"
REEXP["filout"]         = FILOUT
REEXP["filband"]        = FILBAND
REEXP["psband"]         = PSBAND
REEXP["pngband"]        = PNGBAND

"""
ResultPath - class that is responsible for results files
"""
class ResultPath(object):
    def __init__(self, director, simid, linkorder, subtype = None, job = None):
        self._director      = director
        self._simid         = simid     
        self._linkorder     = linkorder
        self._subtype       = subtype
        self._job           = job
        self._init()


    def _init(self):
        "Additional initialization"
        self._resultinfo    = ResultInfo(self._director,
                                         self._simid,
                                         self._linkorder,
                                         subtype = self._subtype,
                                         job = self._job)
        self._jit           = self._resultinfo.jit()


    def resultFiles(self, ftype = None, relative = False):
        """
        Retruns absolute path of the result file(s) specified by file type (ftype), e.g.
        output or input config files, that exist on the file system

        Example: "/home/dexity/exports/vnf/vnfb/content/data/tmp/tmpTsdw21/4ICDAVNK/4I2NPMY4pw.in.out"
        Identifies type of file (e.g. input and output file) based on regular expression (not input record)!

        relative - flag that affects path of returned string. If True, returns
                   results path with respect to dataroot. Used for downloading
                   content.
        Examples:
            relative = True
            returns: "tmp/tmpTsdw21/4ICDAVNK/4I2NPMY4pw.in.out"

            relative = False
            returns: "/home/dexity/exports/vnf/vnfb/content/data/tmp/tmpTsdw21/4ICDAVNK/4I2NPMY4pw.in.out"
        """

        if not ftype:                # All files in the result directory
            return self._allFiles()

        files   = self.filesList()  # Files that exist on the file system
        
        if not ftype in REEXP or not files:   # No entry, no file!
            return None

        file    = self._matchCheck(files, ftype)
        if file:
            if relative:    # Results directory relative to dataroot
                return os.path.join(self._resultinfo.tardir(), file)
            
            # path is not None (verified before!)
            return os.path.join(self.localPath(), file)

        return None


    def filesList(self):
        "Returns list of file names that actually exist on the file system "
        # Example: ["4I2NPMY4pw.in", "4I2NPMY4pw.in.out", "run.sh", ...]
        path    = self.localPath()
        if not path:
            return None

        if os.path.exists(path):
            return self._filesList(path)

        return None


    def localPath(self, relative = False):
        """
        Each job for the task of type will have separate root path specified by
        task type (ttype)

        Example: "/home/dexity/exports/vnf/vnfb/content/data/tmp/tmpTsdw21/4ICDAVNK/
        Note: Result path is assumed not to have child directories.
        """
        if not self._recordsOK():
            return None

        if self._resultinfo.ready():
            if relative:                # If relative path to dataroot
                return self._resultinfo.tardir()

            datadir     = dataroot(self._director)
            return os.path.join(datadir, self._resultinfo.tardir())

        return None     # default case


    def remotePath(self):
        """Returns the path of the jobs directory on the remote server.
        Example: /home/dexity/espresso/qejobs/5YWWTCQT/
        """
        if not self._recordsOK():
            return None

        job     = self._jit[0]

        server  = self._director.clerk.getServers(id=job.serverid)
        if not server:
            return None     # No server, no remote directory

        path    = os.path.join(server.workdir, job.name)
        return os.path.join(path, job.id)


    def _matchCheck(self, files, ftype):
        "Find matching file. Single matching file if possible. Picks first otherwise"
        for fname in files:
            p   = re.compile(REEXP[ftype])
            if p.match(fname):   # matches
                return fname

        return None


    def _allFiles(self):
        "Returns list of *absolute* file names"
        # Example: ["/path/to/results/4I2NPMY4pw.in", "/path/to/results/4I2NPMY4pw.in.out", ...]
        path    = self.localPath()
        if not path:
            return None
        
        if os.path.exists(path):
            return self._files(path)

        return None # Default


    def _files(self, path):
        "Returns list of full file names"
        files       = []
        fileslist   = self._filesList(path)
        for f in fileslist:
            files.append(os.path.join(path, f))

        return files


    def _filesList(self, path):
        "Filters files only and returns list of file names"
        # Example: ["4I2NPMY4pw.in", "4I2NPMY4pw.in.out", "run.sh", ...]
        files   = []
        entries = os.listdir(path)

        for e in entries:   # Filter files
            if os.path.isfile(os.path.join(path, e)):
                files.append(e)

        return files


    def _recordsOK(self):
        "Checks if the proper records exist"
        if not self._jit:         # No jit, no path
            return False

        (job_, input_, task_)   = (self._jit[0], self._jit[1], self._jit[2])  # input_ not used
        # XXX: Return back task_
        if not job_: #or not task_:   # If job or task is None
            return False

        return True

    # Test methods
    def testJit(self):
        return self._jit

__date__ = "$Mar 17, 2010 9:05:14 PM$"


