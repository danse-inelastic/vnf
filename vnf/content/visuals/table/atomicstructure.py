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

from luban.content.table import Model, View, Table
from luban.content import load
from luban.content.Link import Link


class model(Model):

    selected = Model.descriptors.bool(name='selected')
    id = Model.descriptors.str(name='id')
    description = Model.descriptors.link(name='description')
    visualize = Model.descriptors.str(name='visualize')
    chemical_formula = Model.descriptors.str(name='chemical_formula')
    created = Model.descriptors.date(name='created')

    row_identifiers = ['id']
    

columns = [
    View.Column(label='', measure='selected'),
    View.Column(label='ID', measure='id', hidden=True),
    View.Column(label='Description', measure='description'), # editable=True),
    View.Column(label='Chemical_formula', measure='chemical_formula'),
    View.Column(label='Visualize', measure='visualize'),
    View.Column(label='Date created', measure='created'),
    ]


def view(cols, editable=True):
    global columns
    columns = filter(lambda col: col.measure in cols, columns)
    view = View(columns=columns, editable=editable)
    return view


def getSelected(record): return False
def getId(record):
    return record.id
def getDescription(record):
    label = record.short_description
    link = Link(
        label = label,
        onclick = load(
            actor='atomicstructure', routine='showOverview',
            id = record.id,
            )
        )
    return link
def getVisualize(record):
    return 'not implemented'
def getCreated(record):
    date = record.date
    return str(date)
def getChemical_formula(record):
    return record.chemical_formula

def table(atomicstructures, cols, director, editable=True):
    view1 = view(cols, editable=editable)
    
    import operator
    value_generators = [
        eval('get'+col.measure.capitalize())
        for col in view1.columns]
    record2tuple = lambda record: [g(record) for g in value_generators]
    data = map(record2tuple, atomicstructures)
                 
    table = Table(model=model, data=data, 
                  view=view1, id='atomicstructure-table')

    return table

# version
__id__ = "$Id$"

# End of file 
