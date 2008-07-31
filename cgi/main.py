#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def main():


    from vnf.applications.WebApplication import WebApplication


    class MainApp(WebApplication):


        def __init__(self):
            WebApplication.__init__(self, name='main')#, asCGI=True)
            return


    app = MainApp()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    try:
        main()
    except:
        import traceback
        import os
        user = os.environ.get('USER') or 'webserver'
        out = open( '/tmp/vnf-error-%s.log' % user, 'w' )
        out.write( traceback.format_exc() )
    

# version
__id__ = "$Id: main.py,v 1.1.1.1 2006-11-27 00:09:14 aivazis Exp $"

# End of file 
