# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


"""
The scripting interface of vnf.

This provides a high level interface to directly use the http 
vnf server as a service.

It has two ways to run vnf actors.
One is to run vnf main application from command line -- runByCli. 
Another is to run vnf web application by sending http request
to the vnf web server -- runByHttp.
The latter requires setting the variable runByHttp.controller_url.

If using the 1st approach (run app from command line)
all such scripts need to be run in $EXPORT_ROOT/vnf/bin.

See test cases in tests/vnf/scripting for example usages.
"""


def authenticate(username=None, password=None):
    ticket = run(actor='login', routine='authenticate',
        username=username, password=password)
    class C: pass
    c = C()
    c.username = username
    c.ticket = ticket
    return c


def runByCli(actor=None, routine=None, credential=None, **kwds):
    cmd = ['climain.py']
    cmd.append('--actor=%s' % actor)
    cmd.append('--routine=%s' % routine)
    # credential
    if credential:
        cmd.append('--sentry.username=%s' % credential.username)
        cmd.append('--sentry.ticket=%s' % credential.ticket)
        
    for k, v in kwds.iteritems():
        cmd.append('--actor.%s=%s' % (k,v))
        continue

    import sys
    sys.argv = cmd
    from luban.scripts.climain import main
    return main()


class RunByHttp(object):

    from vnf.deployment import controller_url
    
    def __call__(self, actor=None, routine=None, credential=None, **kwds):
        
        # collect arguments
        routine = routine or 'default'
        args = {}
        args['actor'] = actor
        args['routine'] = routine
        # credential
        if credential:
            args['sentry.username'] = credential.username
            args['sentry.ticket'] = credential.ticket

        for k, v in kwds.iteritems():
            args['actor.%s' % k] = v
            continue

        # compose url
        from urllib import urlopen, urlencode
        url = '%s?%s' % (self.controller_url, urlencode(args))

        # open and read
        stream = urlopen(url)
        out = stream.read()
        
        #
        from luban.weaver.web._utils import jsonDecode
        out = jsonDecode(out)
        print out
        return out
runByHttp = RunByHttp()


engine = 'ByHttp'
def run(*args, **kwds):
    m = eval('run%s' % engine)
    return m(*args, **kwds)


def execute(cmd):
    from vnf.utils.spawn import spawn
    return spawn(cmd)


# version
__id__ = "$Id$"

# End of file 
