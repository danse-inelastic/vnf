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


from luban.content.table import Model, View, Table
from luban.content import load
from luban.content.Link import Link


class model(Model):

    selected = Model.descriptors.bool(name='selected')
    id = Model.descriptors.link(name='id')
    description = Model.descriptors.str(name='description')
    type            = Model.descriptors.str(name='type')
    date            = Model.descriptors.date(name='date')

    row_identifiers = ['id', 'type']

columns = [
    View.Column(label='', measure='selected'),
    View.Column(label='ID', measure='id'),
    View.Column(label='Description', measure='description', editable=True),
    View.Column(label='Type', measure='type'),
    View.Column(label='Date created', measure='date'),
    ]


def view(cols, editable=True):
    global columns
    columns = filter(lambda col: col.measure in cols, columns)
    return View(columns=columns, editable=False)


def getSelected(record): return False
def getId(record):
    label = record.id
    link = Link(
        label = label,
        onclick = load(
            actor='sample', routine='view',
            id = record.id,
            type = record.getTableName(),
            )
        )
    return link
def getDescription(record):
    return record.short_description
def getDate(exp):
    date = exp.date
    return str(date)
def getType(matsim):
    return matsim.getTableName()

                
def table(samples, cols, director, editable=True):
    global view
    view = view(cols, editable=editable)

    import operator
    value_generators = [
        eval('get'+col.measure.capitalize())
        for col in view.columns]
    record2tuple = lambda record: [g(record) for g in value_generators]
    data = map(record2tuple, samples)

    table = Table(model=model, data=data, view=view, id='sample-table')

    return table


# version
__id__ = "$Id$"

# End of file 
