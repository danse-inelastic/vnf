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
    """

    def __init__(self, director, job):
        self._director  = director
        self._job       = job   # not None
        self._status    = QEStatus()


    def retrieve(self):
        "Retrievs results based on the status"

        self.status()   # Set status

        if self._status in ["norequest", "oldrequest"]:
            self._startPacking()
            return self.statusstring()



        self._untar()



        return string


    def status(self):
        "Returns status of the simulation without any action (such as results retrieval)"

        # Status changed during results retrieval
        if self._status.get() in [""]:
            return 

        ptrfilepath = self._ptrfilepath()

        # Packing was not requested
        if not os.path.exists(ptrfilepath):
            self._status.set("norequest", "Not Requested")
            return self.statusstring()

        # Packing in progress
        s = open(ptrfilepath).read()
        if s == PackJobDir.PACKINGINPROCESS:
            self._status.set("packing", "Packing In Progress")
            return self.statusstring()

        # Packing is old
        # if tarball old, 
        #    self._status.set("oldrequest", "Outdated Request")
        #    -> "Packing Again"

        # Keep!
#        server      = director.clerk.getServers(id = sim.serverid)
#        jobmtime    = director.dds.getmtime(sim, server = server)   # Requires getmtime.py
#        ptrmtime    = os.path.getmtime(ptrfilepath)
#        if jobmtime > ptrmtime + 60*3: # 60*3 -- give 3 minute of delay
#            # if job directory is newer than the bar ball, pack again
#            self._startPacking(director, sim)
#            link.label  = "Started Packing Again"
#            return link


        s       = open(ptrfilepath).read()
        ss      = s.strip("/")
        if len(ss) != 0 and ss[0] == "tmp":
            return self._tarlink(ptrfilepath)


        return self.statusstring()


    def _norequest(self, ptrfilepath):
        "Packing was not requested"
        if not os.path.exists(ptrfilepath):
            return True

        return False
        

    def _packing(self, ptrfilepath):


    def statusstring(self):
        return self._status.string()


    def _tarlink(self, ptrfilepath):
        text        = "%s.tgz" % self._job.id
        f           = open(ptrfilepath)
        localpath   = f.read().strip()
        path        = "tmp/%s" % localpath      # Example: "tmp/tmp31LUyu/44MTMA42.tgz"
        self._status.setHtmlLink(text, path)
        #link        = HtmlDocument(text="<a href='%s'>%s</a>" % (path, text) )
        #return link
        return self._status.string("html")


    def _ptrfilepath(self):
        """Return pointer filename
        E.g.: /home/dexity/exports/vnf/vnfb/content/data/qejobs/44MTMA42..__dir__pack__ptr__
        """
        PTRFILEEXT = PackJobDir.PTRFILEEXT
        return '.'.join( [self._director.dds.abspath(self._job), PTRFILEEXT] )


    def _untar(self):
        "Untar directory"
        pass

    
    def _startPacking(self):
        from vnf.components.Job import pack
        pack(self._job, self._director, debug=False)
        
        if self._status.get() == "oldrequest":
            # Packing is repeated again
            self._status.set("packingagain", "Packing Again")
        else:
            # Packing has just started
            self._status.set("packing", "Started Packing")
        


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


