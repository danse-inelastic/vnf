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
    created = Model.descriptors.date(name='created')

    row_identifiers = ['id']


columns = [
    View.Column(label='', measure='selected'),
    View.Column(label='ID', measure='id'),
    View.Column(label='Description', measure='description', editable=True),
    View.Column(label='Date created', measure='created'),
    ]

def view(cols, editable=True):
    global columns
    columns = filter(lambda col: col.measure in cols, columns)
    return View(columns=columns, editable=True)


def getSelected(matter): return False
def getId(experiment):
    label = experiment.id
    link = Link(
        label = label,
        onclick = load(
            actor='experiment', routine='showExperimentView',
            id = experiment.id,
            )
        )
    return link
def getDescription(experiment):
    return experiment.short_description
def getCreated(record):
    date = record.date
    return str(date)



def table(experiments, cols, director, editable=True):
    global view
    view = view(cols, editable=editable)
    
    import operator
    value_generators = [
        eval('get'+col.measure[0].upper()+col.measure[1:])
        for col in view.columns]
    record2tuple = lambda record: [g(record) for g in value_generators]
    data = map(record2tuple, experiments)
    
    table = Table(model=model, data=data, view=view, id='experiment-table')
    return table


# version
__id__ = "$Id$"

# End of file 
