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

#The "request" object passed from simple http server
#convert it to a query string
query_string = '&'.join( '%s=%s' % (k, ','.join(v)) for k,v in request.iteritems() )
os.environ['QUERY_STRING'] = query_string

cookie_str = cookie.output(header='', sep=';')
os.environ['HTTP_COOKIE'] = cookie_str


#headers
#print 'headers: %s<br><br>' % headers
#os.environ[ 'CONTENT_TYPE' ] = headers['content-type']


#posted data
#posted = file_handle_for_posted_data.read()
#print posted


from subprocess import Popen, PIPE
p = Popen([webapp], stdout=PIPE, stderr=PIPE)
outdata, errdata = p.communicate()

if p.returncode:
    print errdata
else:
    print outdata[outdata.find('\n')+1:]
    

# version
__id__ = "$Id$"

# End of file 
