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


import luban.content
from TableViewFactoryBase import Factory as base

class Factory(base):


    from vnf.dom.neutron_experiment_simulations.integrated.arcs.ARCSbeam \
        import ARCSbeam as ObjectModel, ARCSbeam_Table
    dbtablename = ARCSbeam_Table.getTableName()
    
    columns = [
        'selected', 'id', 
        'fermi_chopper', 'fermi_nu', 'T0_nu',
        'E', 'emission_time', 'ncount',
        'description', 'date',
        ]
    filtercols = ['id', 'date']
    measure2dbcol = {
        'description': 'short_description',
        }
    sorting_options = [
        ('id', 'ID'),
        ('fermi_chopper', 'Fermi Chopper'),
        ('fermi_nu', "Fermi chopper frequency"),
        ('short_description', 'Description'),
        ('date', 'Date'),
        ]


    def __init__(self, **kwds):
        super(Factory, self).__init__(**kwds)
        
        director = self.director
        self.domaccess = director.retrieveDOMAccessor(
            'instruments/arcs/beamconfiguration')
        return
    

# version
__id__ = "$Id$"

# End of file 
