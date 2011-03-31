# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

bindir='../bin'

def launch_detached(cmd, home='.', debug=False):
    import os
    exe = os.path.abspath(os.path.join(bindir, 'launch-detached.py'))
    home = os.path.abspath(home)
    c = ['%s -cmd="%s" -home=%s' % (exe, cmd, home)]

    if debug: c.append('debug')

    c = ' '.join(c)

    # Move spawn from vnf -> vnfb
    from vnf.utils.spawn import spawn
    import os
    ret, log, err= spawn(c, env=os.environ)
    if ret:
        raise RuntimeError, '%r failed: out=%r, err=%r' % (c, log, err)
    return


def exec_detached(code, home='.'):
    import tempfile
    f = tempfile.mktemp()
    open(f, 'w').write(code)
    cmd = 'python %s; rm -f %s' % (f,f)
    launch_detached(cmd, home=home)
    return


# version
__id__ = "$Id$"

# End of file 
