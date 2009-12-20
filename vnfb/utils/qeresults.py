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

class QEResults:
    """Handles complexity of results of simulation tasks"""

    def __init__(self, director, job):
        self._director  = director
        self._job       = job   # not None


    def retrieve(self):
        "Retrieves results"
        link    = lc.link()

        ptrfilepath = self._ptrfilepath()

        # If pointer file does not exists, need to start packing
        # If it exists the file will not be delivered again
        if not os.path.exists(ptrfilepath):
            self._startPacking()
            link.label  = "Started Packing"
            return link

        # if packing is in process, say that
        s = open(ptrfilepath).read()
        if s == PackJobDir.PACKINGINPROCESS:
            link.label  = "Packing In Progress"
            return link


        self._untar()

        # Keep!
#        server      = director.clerk.getServers(id = sim.serverid)
#        jobmtime    = director.dds.getmtime(sim, server = server)   # Requires getmtime.py
#        ptrmtime    = os.path.getmtime(ptrfilepath)
#        if jobmtime > ptrmtime + 60*3: # 60*3 -- give 3 minute of delay
#            # if job directory is newer than the bar ball, pack again
#            self._startPacking(director, sim)
#            link.label  = "Started Packing Again"
#            return link


        return link


    def status(self):
        "Returns status of the simulation without results retrieval"
        link = self._tarlink(ptrfilepath)
        return


    def _tarlink(self, ptrfilepath):
        text        = "%s.tgz" % self._job.id
        f           = open(ptrfilepath)
        localpath   = f.read().strip()
        path        = "tmp/%s" % localpath      # Example: "tmp/tmp31LUyu/44MTMA42.tgz"
        link        = HtmlDocument(text="<a href='%s'>%s</a>" % (path, text) )

        return link


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


__date__ = "$Dec 20, 2009 11:36:09 AM$"


