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

    # button to skip this wizard
    from . import load_manual_instrument_configuration
    load_manual_configuration = load_manual_instrument_configuration(experiment.id)
    skip_button = lc.button(
        label='skip this wizard',
        onclick=select(element=doc).replaceBy(load_manual_configuration),
        )
    doc.add(skip_button)

    # wizard
    form = doc.form(id='arcs-beam-wizard')
    form.text(name='fermi_nu', label = 'Fermi chopper frequency (Hz)', value=600)
    # form.text(name='fermi_bladeradius', label = 'Fermi choipper blade radius (meter)', value=0.060364)
    form.text(name='T0_nu', label = 'T0 chopper frequency (Hz)', value=120)
    form.text(name='E', label = 'Desired incident energy (meV)', value=100)
    form.text(name='emission_time', label = 'Emission time (microsecond)', value=10)
    form.submitbutton()
    form.onsubmit = select(element=form).submit(
        actor='neutronexperiment/edit/ARCS_beam_withmonitor2_wizard',
        experiment_id = experiment.id)
    
    return doc


# version
__id__ = "$Id$"

# End of file 
