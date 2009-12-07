#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# this script is to be used with the SimpleHttpServer.
# The implementation is crappy.
# SimpleHttpServer is for development test purpose anyway, so
# there is not yet much effort to improve this implementation.


webapp = 'webmain.py'


import os
import pickle

# The "request" object passed from simple http server
os.environ['REQUEST_PICKLED'] = pickle.dumps(request)
# cookie
os.environ['COOKIE_PICKLED'] = pickle.dumps(cookie)



from subprocess import Popen, PIPE
p = Popen([webapp], stdout=PIPE, stderr=PIPE)
outdata, errdata = p.communicate()

if p.returncode:
    print errdata
    print outdata
else:
    print outdata[outdata.find('\n')+1:]
    

# version
__id__ = "$Id$"

# End of file 
