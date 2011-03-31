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
    time_start = Model.descriptors.str(name='time_start')
    state = Model.descriptors.str(name='state')
    
    row_identifiers = ['id']


columns = [
    View.Column(label='', measure='selected'),
    View.Column(label='ID', measure='id'),
    View.Column(label='Description', measure='description', editable=True),
    View.Column(label='Time started', measure='time_start'),
    View.Column(label='Status', measure='state'),
    ]


def view(cols, editable=True):
    global columns
    columns = filter(lambda col: col.measure in cols, columns)
    return View(columns=columns, editable=True)


def getSelected(record): return False
def getId(record):
    label = record.id
    link = Link(
        label = label,
        onclick = load(
            actor='job', routine='view',
            id = record.id,
            )
        )
    return link
def getDescription(record):
    return record.short_description
def getTime_start(record):
    time_start = record.time_start
    return str(time_start)
def getState(record):
    return record.state



def table(jobs, cols, director, editable=True):
    global view
    view = view(cols, editable=editable)
    
    import operator
    value_generators = [
        eval('get'+col.measure.capitalize())
        for col in view.columns]
    record2tuple = lambda record: [g(record) for g in value_generators]
    data = map(record2tuple, jobs)
    
    table = Table(model=model, data=data, view=view, id='job-table')
    return table


# version
__id__ = "$Id$"

# End of file 
