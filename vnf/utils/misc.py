# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import os

def isnewer(path, time):
    mtime = os.path.getmtime(path)
    if mtime >= time: return True
    if os.path.isdir(path):
        entries = os.listdir(path)
        for entry in entries:
            if isnewer(os.path.join(path, entry), time): return True
            continue
    return False


# version
__id__ = "$Id$"

# End of file 
