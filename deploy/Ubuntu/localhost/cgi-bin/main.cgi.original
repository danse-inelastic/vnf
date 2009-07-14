#!/usr/bin/env python
import os

os.system('./envs.sh')

#
# note we still change directory to the 'releaser' cgi directory to access the config folder there
#os.chdir(EXPORT_ROOT+'/vnf/cgi')
from main import main
if __name__ == '__main__':
    # invoke the application shell
    try:
        main()
    except:
        import traceback
        user = os.environ.get('USER') or 'webserver'
        out = open( '/tmp/vnf-error-%s.log' % user, 'w' )
        out.write( traceback.format_exc() )
        
    # sleep just a little to give eclipse time to write out html
    import time
    time.sleep(1)    
    os.system('firefox /home/jbk/DANSE/vnf/html/test.html')
    #user = os.environ.get('USER') or 'webserver'
    #if ('jbk' in user):
    #    os.system('firefox /home/jbk/DANSE/vnf/html/test.html')
