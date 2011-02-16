
from luban.content.table import Model, View, Table
from luban.content import load
from luban.content.Link import Link


class model(Model):

    selectone = Model.descriptors.radio_button(name='selectone')
    id = Model.descriptors.str(name='id')
    description = Model.descriptors.str(name='description')
    visualize = Model.descriptors.link(name='visualize')
    chemical_formula = Model.descriptors.str(name='chemical_formula')
    created = Model.descriptors.str(name='created')

    row_identifiers = ['id']


columns = [
    View.Column(label='', measure='selectone'),
    View.Column(label='ID', measure='id'),
    View.Column(label='Filename', measure='filename'),
    View.Column(label='Description', measure='description', editable=True),
    View.Column(label='Author', measure='creator'),
    View.Column(label='Date created', measure='created'),
    ]


def view(cols, editable=True):
    global columns
    columns = filter(lambda col: col.measure in cols, columns)
    view = View(columns=columns, editable=True)
    return view


def getSelectone(record): return False
def getId(record):
    return record.id
def getDescription(record):
    return record.short_description
def getFilename(record):
    return record.filename
def getCreated(record):
    date = record.date
    return str(date)
def getCreator(record):
    return record.creator


def table(forcefields, cols, director, editable=True):
    view1 = view(cols, editable=editable)
    
    import operator
    value_generators = [
        eval('get'+col.measure.capitalize())
        for col in view1.columns]
    record2tuple = lambda record: [g(record) for g in value_generators]
    data = map(record2tuple, forcefields)

    table = Table(model=model, data=data, view=view1, id='forcefield-table')

    return table


# version
__id__ = "$Id$"

# End of file 
