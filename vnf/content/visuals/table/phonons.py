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


import journal
debug = 'phonons-table'


from luban.content.table import Model, View, Table
from luban.content import load
from luban.content.Link import Link


class model(Model):

    selected = Model.descriptors.bool(name='selected')
    id = Model.descriptors.str(name='id')
    description = Model.descriptors.link(name='description')
    created = Model.descriptors.date(name='created')
    creator = Model.descriptors.str(name='creator')

    row_identifiers = ['id']
    

columns = [
    View.Column(label='', measure='selected'),
    View.Column(label='ID', measure='id', hidden=True),
    View.Column(label='Description', measure='description'), # editable=True),
    View.Column(label='Creator', measure='creator'),
    View.Column(label='Date created', measure='created'),
    ]


def view(cols, editable=True):
    global columns
    columns = filter(lambda col: col.measure in cols, columns)
    view = View(columns=columns, editable=editable)
    return view


class AttrFetcher(object):

    def __init__(self, db, actorname):
        self.db = db
        self.actorname = actorname

    def getSelected(self, record): return False
    
    def getId(self, record):
        return record.id
    
    def getDescription(self, record):
        desc = record.short_description
        if not desc:
            desc = self.createDescription(record)
            
        label = desc
        link = Link(
            label = label,
            onclick = load(
                actor=self.actorname,
                routine='showGraphicalViewWithLinkToTable',
                id = record.id,
                )
            )
        return link
    
    def getCreated(self, record):
        date = record.date
        return str(date)

    
    def getCreator(self, record):
        return record.creator


    def createDescription(self, record):
        db = self.db
        matter = record.matter
        if matter:
            matter = matter.dereference(db)
        if matter is None:
            return 'Unknown'
        matter = matter.short_description or str(matter)
        desc = "Phonons for %s" % matter
        desc = desc[:record.__class__.short_description.length]
        record.short_description = desc
        db.updateRecord(record)
        return desc


    # obsolete
    def createDescription1(self, record):
        db = self.db
        origin = record.getOrigin(db)
        if origin is None:
            return ''
        origin = origin.short_description or str(origin)
        desc = "computed from %s" % origin
        desc = desc[:record.__class__.short_description.length]
        record.short_description = desc
        db.updateRecord(record)
        return desc


def table(records, cols, director, editable=True, actorname=None):
    actorname = actorname or 'material_simulations/phonons'
    
    view1 = view(cols, editable=editable)

    from vnf.dom.Computation import registerAllComputationTables
    registerAllComputationTables(director.clerk)
    attr_fetcher = AttrFetcher(director.clerk.db, actorname)
    import operator
    value_generators = [
        eval('attr_fetcher.get'+col.measure.capitalize())
        for col in view1.columns
        ]
    record2tuple = lambda record: [g(record) for g in value_generators]
    data = map(record2tuple, records)
                 
    table = Table(
        model=model, data=data, 
        view=view1, id='phonons-table')

    return table


# version
__id__ = "$Id$"

# End of file 
