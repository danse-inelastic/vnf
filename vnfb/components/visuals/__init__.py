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

from luban.content import select, load, alert

def set_contextual_help(page='', label=''):
    actions = []
    changepage = select(id='help-page-text').setAttr(value=page)
    actions.append(changepage)
    
    if label:
        changelabel = select(id='help-portlet-about-context').setAttr(label=label)
        actions.append(changelabel)
        
    return actions

# version
__id__ = "$Id$"

# End of file 
