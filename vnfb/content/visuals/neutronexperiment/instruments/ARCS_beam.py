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


import luban.content as lc
from luban.content import load, select, alert

def configuration_wizard(experiment):
    doc = lc.document(
        title='Configuration wizard for ARCS_beam',
        id='instrument-configuration-wizard',
        )

    load_manual_configuration = load(
        actor='loadvisual',
        visual='neutronexperiment/edit/instrumentpanel',
        mode = 'manualconfiguration',
        id=experiment.id
        )
    skip_button = lc.button(
        label='skip',
        onclick=select(element=doc).replaceBy(load_manual_configuration),
        )
    doc.add(skip_button)
    
    return doc


# version
__id__ = "$Id$"

# End of file 
