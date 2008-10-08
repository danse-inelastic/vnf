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

import journal,os
debug = journal.debug('main' )
debug.log(os.environ['PATH'] )
debug.log(os.environ['PYTHONPATH'] )

def assignOrPrepend(paths, environVariable):
    try:
        assert os
        if os.environ.has_key(environVariable):
            os.environ[environVariable] = paths + os.pathsep + os.environ[environVariable]
        else:
            os.environ[environVariable] = paths
    except:
        print '''Error--os has not been imported. os is needed to access a common set of   
        environment variables.  assignOrPrepend() may not work.'''
        #exit()


#Strategy: to make real-time debugging of source code possible and also
# the ability to 'fall back' on older, pythia-installed portions of 
# vnf we simply prepend the source paths to the pythia-path versions.


# original code that simply sets path
#releaser=/home/jbk/DANSE/buildInelast/pyre
#EXPORT_ROOT=$releaser/EXPORT
#python equivalent: 
releaser='/home/jbk/DANSE/buildInelast/pyre'
EXPORT_ROOT=releaser+'/EXPORT'
exportSource='/home/jbk/DANSE/vnf'


# original code that sets environment variables:
#root=/home/jbk/DANSE/buildInelast/pyre/EXPORT
#deps=$root/deps
#
#export PYRE_DIR=$root
#export PATH=$root/bin:$deps/bin:$PATH
#export LD_LIBRARY_PATH=$root/lib:$deps/lib:$LD_LIBRARY_PATH
#export DYLD_LIBRARY_PATH=$root/lib:$deps/lib:$DYLD_LIBRARY_PATH
#export PYTHONPATH=$root/modules:$deps/python:$PYTHONPATH
#source $EXPORT_ROOT/bin/envs.sh
#
# in accord with strategy, we first set the 'releaser' paths
root='/home/jbk/DANSE/buildInelast/pyre/EXPORT'
deps=root+'/deps'
os.environ['PYRE_DIR'] = root
assignOrPrepend(root + '/bin:' + deps + '/bin', 'PATH')
assignOrPrepend(root + '/lib:' + deps + '/lib', 'LD_LIBRARY_PATH')
assignOrPrepend(root + '/lib:' + deps + '/lib', 'DYLD_LIBRARY_PATH')
assignOrPrepend(root + '/modules:' + deps + '/python', 'PYTHONPATH')

#
#
# and then prepend the 'source' paths (to access those preferably and fall back on releaser)
#assignOrPrepend(root + '/bin:' + deps + '/bin', 'PATH')
assignOrPrepend(exportSource,'PYTHONPATH')

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

    try:
        main()
    except:
        import traceback
        import os
        user = os.environ.get('USER') or 'webserver'
        out = open( '/tmp/vnf-error-%s.log' % user, 'w' )
        out.write( traceback.format_exc() )
    
    import time
    time.sleep(1)
    os.system('firefox /home/jbk/DANSE/vnf/html/test.html')

# version
__id__ = "$Id: main.py,v 1.1.1.1 2006-11-27 00:09:14 aivazis Exp $"

# End of file 
