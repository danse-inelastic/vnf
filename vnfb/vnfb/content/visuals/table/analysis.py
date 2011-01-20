#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
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
    #        visualize = Model.descriptors.link(name='visualize')
    #        chemical_formula = Model.descriptors.str(name='chemical_formula')
    #        simulation = Model.descriptors.str(name='simulation')
    creator = Model.descriptors.str(name='creator')
    created = Model.descriptors.date(name='created')

    row_identifiers = ['id']

columns = [
    View.Column(label='', measure='selected'),
    View.Column(label='ID', measure='id'),
    View.Column(label='Description', measure='description', editable=True),
    #        View.Column(label='Visualize', measure='visualize'),
    #        View.Column(label='Chemical_formula', measure='chemical_formula'),
    #        View.Column(label='Simulation', measure='simulation'),
    View.Column(label='Creator', measure='creator'),
    View.Column(label='Date created', measure='created'),
    ]


def view(cols, editable=True):
    global columns
    columns = filter(lambda col: col.measure in cols, columns)
    view = View(columns=columns, editable=editable)
    return view

def getSelected(record): return False
def getId(record):
    label = record.id
    link = Link(
        label = label,
        onclick = load(
            actor='computation', routine='view',
            id = record.id,
            type = record.getTableName(),
            )
        # no need for a redirection
        #    onclick = load(
        #        actor='materialsimulation', routine='showMaterialSimulation',
        #        id = matsim.id,
        #        type = matsim.getTableName(),
        #        )
        )
    return link
def getDescription(record):
    return record.short_description
## def getVisualize(record):
##     return 'not implemented'
## def getChemical_formula(record):
##     return record.chemical_formula
## def getSimulation(record):
##     return 'not implemented'
##     #return record.chemical_formula
def getCreator(record):
    return record.creator
def getCreated(record):
    date = record.date
    return str(date)

def table(analyses, cols, director, editable=True):
    global view
    view = view(cols, editable=editable)
    value_generators = [
        eval('get'+col.measure.capitalize())
        for col in view.columns]
    record2tuple = lambda record: [g(record) for g in value_generators]
    data = map(record2tuple, analyses)
    table = Table(model=model, data=data, 
                  view=view, id='analysis-table')
    return table

# version
__id__ = "$Id$"

# End of file 
