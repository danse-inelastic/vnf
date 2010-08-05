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

# XXX: foxtrot specific
def outdir(director, sim, server, optlevel="0"):
    "Returns temp directory for QE"
    dds     = director.dds
    if int(optlevel) == 0:
        return dds.abspath(sim, server=server)  # Can through exception, handle?

    return ""   # empty string
    #self.


# XXX: foxtrot specific
def createOutdir(director, sim, server, optlevel=0):
    "Returns temp directory for QE"
    dds     = director.dds
    if int(optlevel) == 0:
        dds.makedirs(sim, server=server)  # Can through exception, handle?

    #  director.csaccessor.execute('echo "%s" > %s'

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


