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


"""
base class for visual factories creating tables
"""


import luban.content


from AbstractFactory import AbstractFactory
class TableViewFactory(AbstractFactory):

    """
    factory of a table view including widgets for sorting and filtering
    subclass this class to get custom tables
    
    class variables
    * ObjectModel: dsaw model class
    * columns: names of columns to show
    * descriptors: descriptors of a data object model. for dsaw model, it is model.Inventory.getDescriptors()
    * domaccess: dom accessor
    * dbtablename: db table name
    * filtercols: name of columns with filter support
    * measure2dbcol: map table visual measure name to db column name
    * sorting_options: a list of (name, label) pairs of sorting options
    """
    
    ObjectModel = None 
    columns = None
    descriptors = []
    domaccess = None
    dbtablename = ''
    filtercols = []
    measure2dbcol = {}
    sorting_options = [ ]

    def __init__(self, **kwds):
        super(TableViewFactory, self).__init__(**kwds)

        self.descriptors = self.descriptors or self.ObjectModel.Inventory.getDescriptors()
        self.orm_table_factory = self._createTableFactory()
        self.tableid = "%s-table" % self.name
        return


    def _createTableFactory(self):
        return OrmTableFactory(
            create_single_record_link_action = self.createSingleRecordLinkAction,
            cols = self.columns, descriptors = self.descriptors
            )


    def createSingleRecordLinkAction(self, id):
        return luban.content.load(
            actor=self.actor, 
            routine='view',
            id = id,
            )
    

    def countrecords(self, filter, label=None, mine=False):
        domaccess = self.domaccess
        return domaccess.count(filter, label=label, mine=mine)

    
    def createtable(self, order_by, reverse_order, slice, filter, label=None, mine=False):
        domaccess = self.domaccess
        records = domaccess.getRecords(
            order_by=order_by, 
            reverse_order=reverse_order, 
            slice=slice,
            filter=filter,
            label=label,
            mine=mine,
            )
        return self.orm_table_factory.build(records=records, id=self.tableid)
    

    def build(
        self, 
        filter_expr=None, filter_key=None, filter_value=None,
        label=None, mine=False,
        order_by=None, reverse_order=None,
        number_records_per_page=None, page_number=None,
        ):
        """
        """
        #
        name = self.name
        dbtablename = self.dbtablename
        columns = self.columns
        sorting_options =self.sorting_options
        measure2dbcol = self.measure2dbcol
        filtercols = self.filtercols
        director = self.director
        actor = self.actor
        
        #
        model = self.orm_table_factory.model
        compilefilter = filtercompiler(columns, measure2dbcol, model=model)

        #
        smartlabelaccess = director.retrieveDOMAccessor('smartlabel')
        def filterfromlabel(label):
            return smartlabelaccess.createFilterExprFromLabel(
                label, name)
        smartlabels = smartlabelaccess.getLabelNames(name)

        #
        labelaccess = director.retrieveDOMAccessor('label')
        labels = labelaccess.getLabelNames(name)

        factory = MasterTableFactory(
            name, 
            self.countrecords, self.createtable,
            compilefilter, filtercols,
            filterfromlabel, smartlabels, labels,
            actorname=actor,
            sorting_options = sorting_options,
            polymorphic = False, dbtablename=dbtablename,
            )

        tableview = factory.create(
            label = label, mine = mine,
            filter_expr=filter_expr, filter_key=filter_key, filter_value=filter_value,
            order_by=order_by,
            reverse_order=reverse_order,
            number_records_per_page=number_records_per_page,
            page_number=page_number)
        
        return tableview
from vnf.components.MasterTable import MasterTableFactory, filtercompiler



from luban.orm.table import TableFactory as OrmTableFactoryBase
class OrmTableFactory(OrmTableFactoryBase):


    def __init__(self, create_single_record_link_action=None, **kwds):
        self.create_single_record_link_action = create_single_record_link_action
        super(OrmTableFactory, self).__init__(**kwds)
        return


    def createModel(self):
        from luban.content.table import Model
        base = super(OrmTableFactory, self).createModel()
        class model(base):
            selected = Model.descriptors.bool(name='selected')
            id = Model.descriptors.link(name='id')
            description = Model.descriptors.str(name='description')
            date = Model.descriptors.str(name='date')
            
        return model


    def createCols(self):
        cols = super(OrmTableFactory, self).createCols()
        from luban.content.table import View

        selected_col = View.Column(label='', measure='selected')
        id_col = View.Column(label='ID', measure='id')
        description_col = View.Column(label='Description', measure='description')
        date_col = View.Column(label='Date', measure='date')
        
        cols = [selected_col, id_col, description_col] + cols + [date_col]
        return cols
    
    
    def createValueExtractorClass(self):
        create_single_record_link_action = self.create_single_record_link_action
        from luban.orm.table import createDefaultValueExtractorClass
        import luban.content
        class ValueExtractor(createDefaultValueExtractorClass(self.descriptors)):
            def getSelected(self, record): return False
            def getId(self, record):
                label = record.id
                action = create_single_record_link_action(record.id)
                link = luban.content.link(
                    label = label,
                    onclick = action,
                    )
                return link
            def getDescription(self, record): return record.short_description
            def getDate(self, record): return str(record.date)
        return ValueExtractor


    def createValueExtractor(self):
        klass = self.createValueExtractorClass()
        return klass()

# version
__id__ = "$Id$"

# End of file 
