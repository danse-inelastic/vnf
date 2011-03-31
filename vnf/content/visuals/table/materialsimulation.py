#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2009  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import journal
debug = journal.debug('materialsimulation-table')


from luban.content.table import Model, View, Table
from luban.content import load
from luban.content.Link import Link

class model(Model):

    selected        = Model.descriptors.bool(name='selected')
    id              = Model.descriptors.link(name='id')
    description     = Model.descriptors.str(name='description')
    type            = Model.descriptors.str(name='type')
    matter          = Model.descriptors.str(name='matter')
    created         = Model.descriptors.date(name='created')

    row_identifiers = ['id', 'type']


columns = [
    View.Column(label='', measure='selected'),
    View.Column(label='ID', measure='id'),
    View.Column(label='Description', measure='description', editable=True),
    View.Column(label='Type', measure='type'),
    View.Column(label='Matter', measure='matter'),
    View.Column(label='Date created', measure='created'),
    ]



def view(cols, editable=False):
    global columns
    columns = filter(lambda col: col.measure in cols, columns)
    return View(columns=columns, editable=editable)


class Formatter:

    def __init__(self, db):
        self.db = db
        return

    def getSelected(self, matter): return False
    
    def getId(self, matsim):
        label = matsim.id
        link = Link(
            label = label,
            onclick = load(
                actor='computation', routine='view',
                id = matsim.id,
                type = matsim.getTableName(),
                )
            )
        return link
    
    def getDescription(self, matsim):
        return matsim.short_description
    
    def getCreated(self, exp):
        date = exp.date
        return str(date)
    
    def getType(self, matsim):
        return matsim.getTableName()
    
    def getMatter(self, matsim):
        matter = matsim.matter
        if not matter or not matter.id: return 'not defined'
        try:
            matter = self.db.dereference(matter)
        except:
            import traceback
            debug.log(traceback.format_exc())
            return 'matter %s not found' % matter.id
        identifier = matter.short_description or matter.chemical_formula
        return identifier


def table(matsims, cols, director, editable=True):
    global view
    view = view(cols, editable=editable)

    formatter = Formatter(director.clerk.db)
    
    import operator
    value_generators = [
        getattr(formatter, 'get'+col.measure.capitalize())
        for col in view.columns]
    record2tuple = lambda record: [g(record) for g in value_generators]
    data = map(record2tuple, matsims)

    table = Table(model=model, data=data, view=view, id='matsim-table')
    return table


# version
__id__ = "$Id$"

# End of file 
