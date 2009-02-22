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


class GetdirmtimeApp(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        path = pyre.inventory.str('path', default = '.')


    def main(self, *args, **kwds):
        path = self.path
        
        from filehistory import ModifyHist
        myhist = ModifyHist(path)

        mtimes = myhist.keys()

        if not mtimes: return
        t = mtimes[0]
        print t
        return t


    def __init__(self):
        super(GetdirmtimeApp, self).__init__('getdirmtime')
        return


    def _configure(self):
        super(GetdirmtimeApp, self)._configure()
        self.path = self.inventory.path
        return



def main():
    app = GetdirmtimeApp()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Sat Feb 21 21:09:23 2009

# End of file 
