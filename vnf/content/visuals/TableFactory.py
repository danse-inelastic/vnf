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


    def createValueExtractor(self):
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
        return ValueExtractor()

# version
__id__ = "$Id$"

# End of file 
