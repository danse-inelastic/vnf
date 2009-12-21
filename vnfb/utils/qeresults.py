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
from vnfb.utils.qestatus import QEStatus
from vnf.applications.PackJobDir import PackJobDir


class QEResults:
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
    """

    def __init__(self, director, job):
        self._director  = director
        self._job       = job       # not None
        self._status    = QEStatus()
        self._status.set("norequest", "Not Requested")
        self._ptrfilepath   = self._ptrfilepath()


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
            self._startPacking()
            self._status.set("packingagain", "Packing Again")
            return self._statusstring()
            
#        # Need to untar directory?
#        if self._notuntarred():
#            self._untar()
#            #self._status.set("untarring", "Untarring Results")
#            #return self._statusstring()

        if self._ready():
            self._untar()   # Always untar
            return self._tarlink()
            
        return self._statusstring()


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

        # Outdated packing request
        if self._oldrequest():
            self._status.set("oldrequest", "Outdated Request")
            return self._statusstring()

#        # Need to untar directory?
#        if self._notuntarred():
#            pass
#            #self._status.set("untarring", "Untarring Results")
#            #return self.status()

        if self._ready():
            self._status.set("ready", "Results Ready")
            return self._tarlink()
        
        return self._statusstring()
    

    def _statusstring(self):
        return self._status.string("paragraph")


    def _norequest(self):
        "Packing was not requested before"
        if not os.path.exists(self._ptrfilepath):
            return True

        return False
        

    def _packing(self):
        "Packing in progress"
        s = open(self._ptrfilepath).read()
        if s == PackJobDir.PACKINGINPROCESS:
            return True

        return False


    def _oldrequest(self):
        "Outdated packing request"
        # if tarball old,
        #    self._status.set("oldrequest", "Outdated Request")
        #    -> "Packing Again"

        # Keep!
        #        server      = director.clerk.getServers(id = sim.serverid)
        #        jobmtime    = director.dds.getmtime(sim, server = server)   # Requires getmtime.py
        #        ptrmtime    = os.path.getmtime(self._ptrfilepath)
        #        if jobmtime > ptrmtime + 60*3: # 60*3 -- give 3 minute of delay
        #            # if job directory is newer than the bar ball, pack again
        #            self._startPacking(director, sim)
        #            link.label  = "Started Packing Again"
        #            return link
        return False    # Not supported yet


    def _ready(self):
        "Results are delivered to the server"
        s       = open(self._ptrfilepath).read()
        ss      = s.split("tmp")
        if len(ss) != 0 and ss[0] == '':
            return True

        return False


    def _notuntarred(self):
        "Not relevant. It will untar all the time!"
        #if self._ready() and "directory does not exist or is older than .tgz file":
        #   return True
        #else:
        #   return False
        return True


    def _untar(self):
        #untarring
        pass

    def _tarlink(self):
        text        = "%s.tgz" % self._job.id
        f           = open(self._ptrfilepath)
        localpath   = f.read().strip()
        path        = "tmp/%s" % localpath      # Example: "tmp/tmp31LUyu/44MTMA42.tgz"
        self._status.setHtmlLink(text, path)
        return self._status.string("html")


    def _ptrfilepath(self):
        """Return pointer filename
        E.g.: /home/dexity/exports/vnf/vnfb/content/data/qejobs/44MTMA42..__dir__pack__ptr__
        """
        PTRFILEEXT = PackJobDir.PTRFILEEXT
        return '.'.join( [self._director.dds.abspath(self._job), PTRFILEEXT] )


    def _startPacking(self):
        from vnf.components.Job import pack
        pack(self._job, self._director, debug=False)
        


__date__ = "$Dec 20, 2009 11:36:09 AM$"




# ********************** DEAD CODE **************************

#        #link    = lc.link()
#        #ptrfilepath = self._ptrfilepath()
#
#        # If pointer file does not exists, need to start packing
#        # If it exists the file will not be delivered again
#        if not os.path.exists(ptrfilepath):
#            self._startPacking()
#            self._status.set("Started Packing")
#            return self._status.string()

#            #link.label  = "Started Packing"
#            #return link
#
#        # if packing is in process, say that
#        s = open(ptrfilepath).read()
#        if s == PackJobDir.PACKINGINPROCESS:
#            self._status.set("Packing In Progress")
#            return self._status.string()

            #link.label  = "Packing In Progress"
            #return link


