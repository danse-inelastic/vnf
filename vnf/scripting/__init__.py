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

It basically run vnf main application from command line, and that
is just like someone clicking mouse.

all such scripts need to be run in $EXPORT_ROOT/vnf/bin
"""


def authenticate(username=None, password=None):
    ticket = run(actor='login', routine='authenticate',
        username=username, password=password)
    class C: pass
    c = C()
    c.username = username
    c.ticket = ticket
    return c


def run(actor=None, routine=None, credential=None, **kwds):
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


def run1(actor=None, routine=None, credential=None, **kwds):
    routine = routine or 'default'
    cmd = ['climain.py --actor=%s --routine=%s' % (actor, routine)]
    # credential
    if credential:
        cmd.append('--sentry.username=%s' % credential.username)
        cmd.append('--sentry.ticket=%s' % credential.ticket)
        
    for k, v in kwds.iteritems():
        cmd.append('--actor.%s="%s"' % (k,v))
        continue
    cmd = ' '.join(cmd)
    print cmd
    ret, out, err = execute(cmd)
    if ret:
        msg = '%s failed.\nOUT: %s\nERROR: %s\n' % (
            ret, out, err)
        raise RuntimeError, msg
    return out.strip()


def execute(cmd):
    from vnf.utils.spawn import spawn
    return spawn(cmd)


# version
__id__ = "$Id$"

# End of file 
