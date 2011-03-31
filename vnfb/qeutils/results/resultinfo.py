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
import time
from vnf.components.Job import pack
from vnf.qeutils.message import Message
from vnf.applications.PackJobDir import PackJobDir
from vnf.qeutils.qeconst import RESULTS_ID
from vnf.qeutils.qerecords import SimulationRecord
from vnf.qeutils.qeutils import ifelse

import luban.content as lc
from luban.content import load

DELAY       = 60*1  # 1 minute delay
CLASS_ERROR = 'qe-text-red'
CLASS_OK    = 'qe-text-blue'
CLASS_NA    = 'qe-text-black'

# XXX: Needs severe refactoring
class ResultInfo:
    """
    Handles complexity of job results
    There are the following supported states:
        norequest   - No request has been sent for packing the results
        started     - Packing has just started
        packing     - Packing on progress
        oldrequest  - Outdated request
        packingagain    - Packing started again
        untarring   - Untar the simulation results
        ready       - Results are ready for analysis

    Notes:
        - The reason why I separate two methods: retrieve() and status() is because I have
          at least two types of triggers: 1) check results and 2) show results
        - Results link is specified by id
    """

    # XXX: Remove task or input?
    def __init__(self, director, simid, linkorder, job = None, subtype = None, task = None, input = None):
        self._director  = director
        self._simid     = simid
        self._linkorder = linkorder
        self._task      = task
        self._input     = input
        self._job       = job
        self._subtype   = subtype

        self._init()
        self._status    = Message()
        self._status.set("norequest", "Not Requested")
        self._ptrfilepath   = self._ptrfilepath()


    def _init(self):
        "Additional init"
        self._simrecord   = SimulationRecord(self._director, self._simid, self._subtype)
        if not self._task:
            self._task = self._simrecord.task(self._linkorder)

        if not self._input:
            self._input = self._simrecord.input(self._linkorder)
            
        if not self._job:
            self._job   = self._simrecord.job(self._linkorder)


    def simrecord(self):
        "Returns simulation record object"
        return self._simrecord


    def jit(self):
        "Returns (job, input, task) tuple"
        return (self._job, self._input, self._task)


    def retrieve(self):
        "Retrievs results based on the status"

        self.status()
        
        # Packing was not requested before
        if self._norequest():
            self._startPacking()
            self._status.set("started", "Started Packing")
            return self._statusstring()

        # Outdated packing request
        if self._oldrequest():
            # If job directory is newer than the tar ball, pack again
            self._startPacking()
            self._status.set("packingagain", "Packing Again")
            return self._statusstring()

        if self.ready():
            self._untar()   # Always untar
            return self._tarlink()
            
        return self._statusstring()


#        # Need to untar directory?
#        if self._notuntarred():
#            self._untar()
#            #self._status.set("untarring", "Untarring Results")
#            #return self._statusstring()


    def status(self):
        "Returns status of the simulation without any action (such as results retrieval)"
        # Packing was not requested before

        if self._norequest():
            self._status.set("norequest", "Not Requested")
            return self._statusstring()

        # Packing in progress
        if self._packing():
            self._status.set("packing", "Packing In Progress")
            return self._statusstring()

        if self.ready():
            self._status.set("ready", "Results Ready")
            return self._tarlink()
        
        return self._statusstring()


    def stateLabel(self):
        return self._status.stateLabel()

#        # Outdated packing request # Don't need?
#        if self._oldrequest():
#            self._status.set("oldrequest", "Outdated Request")
#            return self._statusstring()

#        # Need to untar directory?
#        if self._notuntarred():
#            self._status.set("untarring", "Untarring Results")
#            return self.status()


    def link(self):
        """
        Returns link to results when ready or string with status
        """
        cid         = "%s-%s" % (RESULTS_ID, self._id()) # self._task.id?
        container   = lc.document(id=cid)
        link        = lc.htmldocument(text="None") # Default value

        if self._job:
            link    = self.status()
            
        container.add(link)
        return container


    def action(self):
        "Returns link to action that refreshes the status of results"
        if not self._job: #or not self._task:
            return ""   # Default value

        return lc.link(label = "Check",
                       id = "qe-check-results",
                       onclick=load(actor       = "jobs/getresults",
                                    routine     = "retrieveStatus",
                                    id          = self._simid,
                                    taskid      = self._task.id,
                                    jobid       = self._job.id)
                  )


    def _statusstring(self):
        self._status.setClass(CLASS_NA)     # Default class for status string
        return self._status.string("div")


    def _norequest(self):
        "Packing was not requested before"
        if self._ptrfilepath and not os.path.exists(self._ptrfilepath):
            return True

        return False
        

    def _packing(self):
        "Packing in progress"
        if self._ptrfilepath and os.path.exists(self._ptrfilepath):
            s = open(self._ptrfilepath).read()
            if s == PackJobDir.PACKINGINPROCESS:
                return True

        return False


    def _oldrequest(self):
        """
        Outdated packing request. Implemented in case if results delivery failed.
        It can trigger packing from remote server
        """
        server      = self._director.clerk.getServers(id = self._job.serverid)
        # Don't understand what's the point
        #jobmtime    = self._director.dds.getmtime(self._job, server = server)   # Requires getmtime.py

        ptrmtime    = os.path.getmtime(self._ptrfilepath)  
        curtime     = time.time()

        if curtime > ptrmtime + DELAY:  # 1 minute of delay
            return True

        return False


    def ready(self):
        "Results are delivered to the server"

        if self._ptrfilepath and os.path.exists(self._ptrfilepath):
            s       = open(self._ptrfilepath).read()
            ss      = s.split("tmp")
            if len(ss) != 0 and ss[0] == '':
                return True

        return False


    def _setResultClass(self):
        """
        When results are ready, check if there is error (e.g. crash file) and
        change status class
        """
        # Import should be local
        
        Class       = CLASS_OK
        from vnf.qeutils.results.resultpath import ResultPath
        resultpath  = ResultPath(self._director, self._simid, self._linkorder)
        fcrash      = resultpath.resultFiles("crash")
        if fcrash:
            Class   = CLASS_ERROR
            
        self._status.setClass(Class)


    def _notuntarred(self):
        "Not relevant. It will untar all the time!"
        #if self.ready() and "directory does not exist or is older than .tgz file":
        #   return True
        #else:
        #   return False
        return True


    def _untar(self):
        dds = self._director.dds
        # Example: dataroot = /home/dexity/exports/vnf/vnf/content/data
        dataroot    = os.path.abspath(dds.dataroot) # Absolute data root

        tarfile     = os.path.join(dataroot, self._tarpath())
        tempdir     = os.path.join(dataroot, self._tempdir())

        dds.untar(tarfile, tempdir)
        

    def _tarlink(self):
        text    = self._tarfile()
        path    = self._tarpath()
        self._setResultClass()
        self._status.setHtmlLink(text, path)
        return self._status.string("a")


    def _tarfile(self):
        "Tar file"
        return "%s.tgz" % self._job.id      # Example: "44MTMA42.tgz"


    def _tarpath(self):
        "Path to tar file is expected"
        f           = open(self._ptrfilepath)
        localpath   = f.read().strip()
        return "tmp/%s" % localpath      # Example: "tmp/tmp31LUyu/44MTMA42.tgz"


    def tardir(self):
        "Returns path to untarred directory with results"
        path    = self._tarpath()
        parts   = path.split(".tgz")
        dir     = parts[0]
        return dir                      # Example: "tmp/tmp31LUyu/44MTMA42"


    def _tempdir(self):
        path    = self._tarpath()
        parts   = path.split(self._tarfile())
        tmp     = parts[0]
        return tmp                      # Example: "tmp/tmp31LUyu


    def _id(self):
        jobid   = self._linkorder
        if self._job:
            jobid   = self._job.id

        return jobid   


    def _ptrfilepath(self):
        """Return pointer filename
        E.g.: /home/dexity/exports/vnf/vnf/content/data/qejobs/44MTMA42..__dir__pack__ptr__
        """
        if not self._job:
            return
        
        PTRFILEEXT = PackJobDir.PTRFILEEXT
        return '.'.join( [self._director.dds.abspath(self._job), PTRFILEEXT] )


    def _startPacking(self):
        pack(self._job, self._director, debug=False)
        


__date__ = "$Dec 20, 2009 11:36:09 AM$"
