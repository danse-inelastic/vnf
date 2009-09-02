#!/usr/bin/env python
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


from pyre.applications.Script import Script


class GetmtimeApp(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        path = pyre.inventory.str('path', default = '.')


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


    def __init__(self):
        super(GetmtimeApp, self).__init__('getmtime')
        return


    def _configure(self):
        super(GetmtimeApp, self)._configure()
        self.path = self.inventory.path
        return


import os


def main():
    app = GetmtimeApp()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Sat Feb 21 21:09:23 2009

# End of file 
