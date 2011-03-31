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
    date = Model.descriptors.str(name='date')
    fermi_chopper = Model.descriptors.str(name='fermi_chopper')
    fermi_nu = Model.descriptors.str(name='fermi_nu')
    T0_nu = Model.descriptors.str(name='T0_nu')
    E = Model.descriptors.str(name='E')
    emission_time = Model.descriptors.str(name='emission_time')
    ncount = Model.descriptors.str(name='ncount')
    
    row_identifiers = ['id']


columns = [
    View.Column(label='', measure='selected'),
    View.Column(label='ID', measure='id'),
    View.Column(label='Fermi chopper', measure='fermi_chopper'),
    View.Column(label='Fermi chopper frequency', measure='fermi_nu'),
    View.Column(label='T0 chopper frequency', measure='T0_nu'),
    View.Column(label='Energy', measure='E'),
    View.Column(label='Emission time', measure='emission_time'),
    View.Column(label='Number of neutrons', measure='ncount'),
    View.Column(label='Description', measure='description', editable=True),
    View.Column(label='Date', measure='date'),
    ]

allcols = [c.measure for c in columns]

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
            actor='instruments/arcs/beam-profile', routine='view',
            id = record.id,
            )
        )
    return link
def getDescription(record):
    return record.short_description


def createValStrGetter(prop):
    try:
        f = eval('get'+prop.capitalize())
    except:
        def _(record):
            v = getattr(record, prop)
            return str(v)
        f = _
    return f


def table(jobs, cols=None, director=None, editable=True):
    cols = cols or allcols
    
    global view
    view = view(cols, editable=editable)
    
    import operator
    value_generators = [
        createValStrGetter(col.measure)
        for col in view.columns
        ]
    record2tuple = lambda record: [g(record) for g in value_generators]
    data = map(record2tuple, jobs)
    
    table = Table(model=model, data=data, view=view, id='arcsbeamprofile-table')
    return table


# version
__id__ = "$Id$"

# End of file 
