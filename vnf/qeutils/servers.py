# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

"""
Server specific configurations

Attempt to keep server specific settings in one place: probably will need
refactoring to a database or configuration files (e.g.: .pml)
"""
import os

serverlist = {"foxtrot": {  "address":      "foxtrot.danse.us",
                            "username":     "danse-vnf-admin",
                            "workdir":      "/home/danse-vnf-admin/vnf/data",
                            "outdir":       "/scratch/vnf"
                         },
              # There is some issue with indirection: [local] -> [cacr.caltech.edu] -> [octopod]
              # ssh -tAX dexity@login.cacr.caltech.edu ssh -tAX octopod.danse.us
              "octopod": {  "address":      "octopod.danse.us",
                            "username":     "danse-vnf-admin",
                            "workdir":      "/home/danse-vnf-admin/vnf/data",
                            "outdir":       "/home/danse-vnf-admin/vnf/data"
                         },
}

DEFAULT = ""
MKDIR   = "%s bash -c \"if [ ! -d '%s' ]; then mkdir -p '%s'; fi;\""

# XXX: foxtrot specific
# XXX: Can through an exception, handle?
def outdir(director, sim, server, optlevel="0"):
    """
    Returns temp directory for QE
    
    opt = 0: /home/danse-vnf-admin/vnf/data/qesimulations/3YEQ8PNV
    opt = 1: /scratch/vnf/3YEQ8PNV
    """
    if not sim:     # No None simulation
        return DEFAULT

    dds     = director.dds
    if int(optlevel) == 0:
        return dds.abspath(sim, server=server)  # Can through exception, handle?

    if int(optlevel) == 1:
        basedir = serverlist["foxtrot"]["outdir"]
        return os.path.join(basedir, sim.id)

    return DEFAULT   # empty string



# XXX: Can through an exception, handle?
def createOutdir(director, sim, server, optlevel=0, cmd=MKDIR, shell="bpsh -a"):
    """Returns temp directory for QE
    
    Example:
        cmd     = "bpsh -a bash -c \"if [ ! -d '%s' ]; then mkdir -p '%s'; fi;\"" % (dir, dir)
    Notes:
        - Set either cmd or shell
        
    """
    if not sim:     # No None simulation
        return DEFAULT

    dds     = director.dds
    if int(optlevel) == 0:
        dds.makedirs(sim, server=server)  

    if int(optlevel) == 1:
        basedir = serverlist["foxtrot"]["outdir"]
        dir     = os.path.join(basedir, sim.id)
        # Magic line for checking is directory exists and creating one, if not
        cmdstr  = ""
        if cmd:
            cmdstr  = cmd % (shell, dir, dir)
        director.csaccessor.execute(cmdstr, server, "")


#class Server:
#
#    def __init__(self, dds, sim, server):
#        self._dds       = dds
#        self._sim       = sim
#        self._server    = server
#
#
#    def outdir(self):
#        pass
#
#    def createOutdir(self):
#        pass

__date__ = "$Aug 4, 2010 10:37:06 AM$"


