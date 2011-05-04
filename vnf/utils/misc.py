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

def isnewer(path, time,
            getmtime=os.path.getmtime,
            isdir=os.path.isdir,
            listdir=os.listdir,
            ):
    mtime = getmtime(path)
    if mtime >= time: return True
    if isdir(path):
        entries = listdir(path)
        for entry in entries:
            if isnewer(os.path.join(path, entry), time,
                       getmtime=getmtime, isdir=isdir, listdir=listdir): return True
            continue
    return False



def most_recent_file(directory):
    'find the most recent file in the given directory'
    files = [os.path.join(directory, entry) for entry in os.listdir(directory)]

    getctime = os.path.getctime
    def comp(f1, f2):
        timediff = getctime(f1) - getctime(f2)
        if timediff<0: return -1
        if timediff>0: return 1
        return 0

    files.sort(comp)

    return files[-1]


# version
__id__ = "$Id$"

# End of file 
