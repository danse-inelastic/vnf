#!/usr/bin/env python
import os

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


#original code
#cd $EXPORT_ROOT/vnf/cgi && python main.py $@
#
# note we still change directory to the 'releaser' cgi directory to access the config folder there
#os.chdir(EXPORT_ROOT+'/vnf/cgi')
from main import main
if __name__ == '__main__':
    # invoke the application shell
    try:
    	print os.environ['PYTHONPATH']
        main()
    except:
        import traceback
        user = os.environ.get('USER') or 'webserver'
        out = open( '/tmp/vnf-error-%s.log' % user, 'w' )
        out.write( traceback.format_exc() )
        
    os.system('firefox /home/jbk/DANSE/vnf/html/test.html')
    #user = os.environ.get('USER') or 'webserver'
    #if ('jbk' in user):
    #    os.system('firefox /home/jbk/DANSE/vnf/html/test.html')
