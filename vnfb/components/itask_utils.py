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

def start(task, debug=False):
    from vnf.utils import launch_detached, bindir
    import os
    cmd = os.path.join(bindir, task_runner)

    options = {
        'iworker': task.worker,
        'id': task.id,
        }

    extra_options = task.options
    for i in range(len(extra_options)/2):
        k = 'iworker.%s' % extra_options[2*i]
        v = extra_options[2*i+1]
        options[k] = v
        continue

    optstr = ' '.join(
        [ '--%s="%s"' % (k,v) for k,v in options.iteritems() ])
    cmd += ' ' + optstr

    launch_detached(cmd, debug=debug)
    return


def progressbarID(task):
    return 'itask-%s-pbar' % task.id


task_runner = 'itaskapp.py'


# version
__id__ = "$Id$"

# End of file 
