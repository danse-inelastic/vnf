# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

def announcement():
    from Announcement import Announcement
    return Announcement()


def safe_eval_action(s):
    """evaluate an luban action

    e.g. safe_eval_action('load(actor="login")')
    """
    s = 'action=%s' % s
    from luban.content import load, alert, select
    c = {
        'action': None, 
        'load': load,
        'alert': alert,
        'select': select,
        }
    from vnfb.utils.safe_eval import safe_eval
    safe_eval(s, c)
    return c['action']


# version
__id__ = "$Id$"

# End of file 
