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
from TableViewFactoryBase import Factory as base, OrmTableFactory as OrmTableFactoryBase

class Factory(base):


    from vnf.dom.neutron_experiment_simulations.integrated.arcs.ARCSIQEResolutionComputation import \
        ARCSIQEResolutionComputation as ObjectModel, \
        ARCSIQEResolutionComputation_Table as Table
    dbtablename = Table.getTableName()
    
    columns = [
        'selected', 'id', 
        'Q', 'E',
        'dQ', 'dE',
        'neutronsatsample',
        'ncount',
        'description', 'date',
        ]
    filtercols = ['id', 'date']
    measure2dbcol = {
        'description': 'short_description',
        }
    sorting_options = [
        ('id', 'ID'),
        ('short_description', 'Description'),
        ('date', 'Date'),
        ]


    def __init__(self, **kwds):
        super(Factory, self).__init__(**kwds)
        
        director = self.director
        self.domaccess = director.retrieveDOMAccessor(
            'instruments/arcs/iqeresolutioncomputation')
        return
    
    
    # for customization of table factory
    def _createTableFactory(self):
        factory = OrmTableFactory(
            director = self.director,
            create_single_record_link_action = self.createSingleRecordLinkAction,
            cols = self.columns, descriptors = self.descriptors
            )
        return factory


# for customization of column "neutronsatsample"
class OrmTableFactory(OrmTableFactoryBase):


    def __init__(self, director=None, **kwds):
        self.director = director
        super(OrmTableFactory, self).__init__(**kwds)
        return

    
    def createValueExtractorClass(self):
        director = self.director
        base = super(OrmTableFactory, self).createValueExtractorClass()
        class ValueExtractor(base):
            def getNeutronsatsample(self, record):
                db = director.clerk.db
                nas = record.neutronsatsample
                if nas:
                    return nas.dereference(db).short_description
                return 'None'
        return ValueExtractor


# version
__id__ = "$Id$"

# End of file 
