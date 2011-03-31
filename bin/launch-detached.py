#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def main(**kwds):


    from vnfb.applications.LaunchDetached import Launch


    class App(Launch):


        def help(self):
            super(App, self).help()
            import sys
            print
            print '* Debug:'
            print
            print '  $ %s <...options...> debug ' % sys.argv[0]
            return
        

        def _getPrivateDepositoryLocations(self):
            return ['../config']


    app = App('launch-detached')
    return app.run(**kwds)


# main
if __name__ == '__main__':
    import sys
    argv = sys.argv
    last = argv[-1]
    if last == 'debug':
        # invoke the application shell
        main(spawn=0)
    else:
        main()
        


# version
__id__ = "$Id$"

# End of file 
