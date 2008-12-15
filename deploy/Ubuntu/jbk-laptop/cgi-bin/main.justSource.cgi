#!/usr/bin/env python

#Strategy: to make real-time debugging of source code possible and also
# the ability to 'fall back' on older, pythia-installed portions of 
# vnf we simply prepend the source paths to the pythia-path versions.


# original code that simply sets path
#releaser=/home/jbk/DANSE/buildInelast/pyre
#EXPORT_ROOT=$releaser/EXPORT
#python equivalent: 
EXPORT_ROOT='/home/jbk/DANSE'

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
# python equivalent:
import os
pythiaInstallation='/home/jbk/dv/tools/pythia-0.8'
deps=pythiaInstallation+'/deps'
os.environ['PYRE_DIR'] = pythiaInstallation
os.environ['PATH'] = pythiaInstallation + '/bin:' + deps + '/bin:' + os.environ['PATH']
if os.environ.has_key('LD_LIBRARY_PATH'):
	os.environ['LD_LIBRARY_PATH'] = pythiaInstallation + '/lib:' + deps + '/lib:' + os.environ['LD_LIBRARY_PATH']
else:
	os.environ['LD_LIBRARY_PATH'] = pythiaInstallation + '/lib:' + deps + '/lib'
if os.environ.has_key('DYLD_LIBRARY_PATH'):
	os.environ['DYLD_LIBRARY_PATH'] = pythiaInstallation + '/lib:' + deps + '/lib:' + os.environ['DYLD_LIBRARY_PATH']
else:
	os.environ['DYLD_LIBRARY_PATH'] = pythiaInstallation + '/lib:' + deps + '/lib'
if os.environ.has_key('PYTHONPATH'):
	os.environ['PYTHONPATH'] = pythiaInstallation + '/modules:' + deps + '/python:' + os.environ['PYTHONPATH']
else:
	os.environ['DYLD_LIBRARY_PATH'] = pythiaInstallation + '/modules:' + deps + '/python:'
# note: notice we do not use the 'deployed' version of vnf that has been
# copied to the pyre dv which is linked to buildInelast.  Rather, we
# use the source version by setting the paths directly to that.  And we set paths to pyre and vnf 
# in the eclipse project rather than here so all the above is commented out. 

#original code
#cd $EXPORT_ROOT/vnf/cgi && python main.py $@
os.chdir(EXPORT_ROOT+'/vnf/cgi')
from main import main
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
        
    import os
    user = os.environ.get('USER') or 'webserver'
    if ('jbk' in user):
        os.system('firefox /home/jbk/DANSE/vnf/html/test.html')
