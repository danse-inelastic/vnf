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

"""
Non-pyre version of getmtime.py script that returns time of lastly modified file
or directory. This is useful to use on remote server where pyre is not installed
"""

class Getmtime:

    def __init__(self):
        pass

    def main(self, *args, **kwds):
        path = self.path

        if not os.path.exists(path): return

        if os.path.isdir(path):
            mtime = self._handle_dir(path)
        else:
            mtime = self._handle_file(path)

        print mtime
        return mtime


    def _handle_file(self, path):
        return os.path.getmtime(path)


    def _handle_dir(self, path):
        from filehistory import ModifyHist
        myhist = ModifyHist(path)

        mtimes = myhist.keys()

        if not mtimes: return os.path.getmtime(path)
        return mtimes[0]


__date__ = "$Jan 8, 2010 5:54:45 PM$"


