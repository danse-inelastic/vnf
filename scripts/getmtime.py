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

import os

usage   = """Usage:
    getmtime.py --path=/path/to/something
Make sure that directory of getmtime.py is in $PATH
"""

class Getmtime:

    def __init__(self):
        import sys
        argv    = sys.argv
        
        # If number of arguments is not equal to two,
        # or second argument does not have "=" character
        if len(argv) != 2:
            print usage
            return
            
        if len(argv) == 2:
            s   = argv[1]
            ss  = s.split("=")
            if len(ss) != 2 or ss[1] == '':
                print usage
                return

        # Arguments are corrent
        ss          = argv[1].split("=")
        self.path   = ss[1]


    def get(self):
        "Print the time"
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

if __name__ == "__main__":
    time = Getmtime()
    time.get()
    
#    import time
#    print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(1249069869))

