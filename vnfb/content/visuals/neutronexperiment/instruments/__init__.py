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


def load_manual_instrument_configuration(experiment_id):
    from luban.content import load
    return load(
        actor='loadvisual',
        visual='neutronexperiment/edit/instrumentpanel',
        mode = 'manualconfiguration',
        id=experiment_id
        )


# version
__id__ = "$Id$"

# End of file 
