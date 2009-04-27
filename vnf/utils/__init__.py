# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
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
    #print c

    from spawn import spawn
    import os
    ret, log, err= spawn(c, env=os.environ)
    if ret:
        raise RuntimeError, '%r failed: out=%r, err=%r' % (c, log, err)
    return

# Converts URL to UTF-8 encoded characters
def unquote_unicode(source):
    import urllib
    result = urllib.unquote(source)
    print result
    if '%u' in result:
        result = result.replace('%u','\\u').decode('unicode_escape')
    return result


# version
__id__ = "$Id$"

# End of file 
