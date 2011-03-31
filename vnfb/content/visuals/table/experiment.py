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
debug = journal.debug('experiment-table')


from luban.content.table import Model, View, Table
from luban.content import load
from luban.content.Link import Link

class model(Model):

    selected = Model.descriptors.bool(name='selected')
    id = Model.descriptors.link(name='id')
    description = Model.descriptors.str(name='description')
    sample = Model.descriptors.str(name='sample')
    created = Model.descriptors.date(name='created')

    row_identifiers = ['id']


columns = [
    View.Column(label='', measure='selected'),
    View.Column(label='ID', measure='id'),
    View.Column(label='Description', measure='description', editable=True),
    View.Column(label='Sample', measure='sample'),
    View.Column(label='Date created', measure='created'),
    ]

def view(cols, editable=True):
    global columns
    columns = filter(lambda col: col.measure in cols, columns)
    return View(columns=columns, editable=True)


class Formatter:

    def __init__(self, db):
        self.db = db
        return

    def getSelected(self, matter): return False
    
    def getId(self, experiment):
        label = experiment.id
        link = Link(
            label = label,
            onclick = load(
                actor='experiment', routine='showExperimentView',
                id = experiment.id,
                )
            )
        return link
    
    def getDescription(self, experiment):
        return experiment.short_description
    
    def getSample(self, experiment):
        return experiment.sample 
        
    def getCreated(self, record):
        date = record.date
        return str(date)



def table(experiments, cols, director, editable=True):
    global view
    view = view(cols, editable=editable)
    
    formatter = Formatter(director.clerk.db)

    import operator
    value_generators = [
        getattr(formatter, 'get'+col.measure.capitalize())
        for col in view.columns]
    record2tuple = lambda record: [g(record) for g in value_generators]
    data = map(record2tuple, experiments)
    
    table = Table(model=model, data=data, view=view, id='experiment-table')
    return table


# version
__id__ = "$Id$"

# End of file 
