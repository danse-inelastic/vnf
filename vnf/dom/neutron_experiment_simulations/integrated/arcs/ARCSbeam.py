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


class ARCSbeam:

    fermi_chopper = '100-1.5-SMI'
    fermi_nu = 600
    T0_nu = 60
    E = 70
    emission_time = -1
    ncount = 1e9
    
    # key properties
    # if values for key properties are the same, the two
    # objects can be regarded as the same
    key_props = [
        'fermi_chopper',
        'fermi_nu', 'T0_nu', 'E', 'emission_time', 
        'ncount',
        ]
    
    def customizeLubanObjectDrawer(self, drawer):
        drawer.mold.sequence = [
            'fermi_chopper',
            'fermi_nu',
            'T0_nu',
            'E',
            'emission_time',
            'ncount',
            ]
        return


fc_choices = [
    '100-1.5-SMI',
    '700-1.5-SMI',
    '700-0.5-AST',
    ]

from dsaw.model.Inventory import Inventory as InvBase

class Inventory(InvBase):

    fermi_chopper = InvBase.d.str(name='fermi_chopper', default='100-1.5-SMI')
    fermi_chopper.label = 'Select a Fermi chopper'
    fermi_chopper.validator = InvBase.v.choice(fc_choices)

    fermi_nu = InvBase.d.float(name='fermi_nu', default=600)
    fermi_nu.label = 'Fermi chopper frequency (Hz)'
    fermi_nu.validator = InvBase.v.choice([600,480,300])
    
    T0_nu = InvBase.d.float(name='T0_nu', default=60)
    T0_nu.validator = InvBase.v.positive
    T0_nu.label = 'T0 chopper frequency (Hz)'
    T0_nu.expert = True
    
    E = InvBase.d.float(name='E', default=70)
    E.label = 'Norminal incident energy (meV)'
    E.validator = InvBase.v.isBoth(InvBase.v.greaterEqual(0.1), InvBase.v.less(1e5))
    
    emission_time = InvBase.d.float(name='emission_time', default=-1)
    emission_time.label = 'Emission time (microsecond)'
    emission_time.expert = True
    
    ncount = InvBase.d.int(name='ncount', default=10000000,
                           validator = InvBase.v.greaterEqual(1000000),
                           )
    ncount.label = 'number of Monte Carlo simulation runs' #. Each MC run corresponds to 34kJ energy.'
    ncount.expert = True
    
    dbtablename = 'arcsbeamconfigurations'


ARCSbeam.Inventory = Inventory

from vnf.dom._ import o2t
from vnf.dom.Computation import Computation
ARCSbeam_Table = o2t(ARCSbeam, {'subclassFrom': Computation})
ARCSbeam_Table.job_builder = 'mcvine/arcs/beam-profile'
ARCSbeam_Table.actor = 'instruments/arcs/beam-profile'
ARCSbeam_Table.result_retriever = 'mcvine/arcs/beam-profile'


# version
__id__ = "$Id$"

# End of file 
