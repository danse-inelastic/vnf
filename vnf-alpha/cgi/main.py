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


def suppressWarnings():
    import warnings
    categories_to_ignore = [
        DeprecationWarning,
        Warning,
        ]
    for category in categories_to_ignore:
        warnings.filterwarnings('ignore', category=category)

    import journal
    journal.error('pyre.inventory').deactivate()
    return
suppressWarnings()



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
        import journal,os
        debug = journal.debug('main' )
        debug.log(os.environ['PATH'] )
        debug.log(os.environ['PYTHONPATH'] )

        main()
    except:
        errorlogfile = '../log/errors.log'

        import traceback, time
        t = time.ctime()
        messages = [
            '[%s]' % t,
            ]
        messages += traceback.format_exc().split('\n')
        
        out = open(errorlogfile, 'a' )
        out.write( '\n'.join(messages))
        
    # debugging hack by brandon    
    if os.environ.has_key('USER'):
        if 'jbk' in os.environ['USER']:
            os.system('firefox-3.5 ../html/test.html')
    

# version
__id__ = "$Id: main.py,v 1.1.1.1 2006-11-27 00:09:14 aivazis Exp $"

# End of file 
