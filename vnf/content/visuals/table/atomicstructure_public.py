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


from atomicstructure import *

# overload link
def getDescription(record):
    label = record.short_description
    id = record.id
    from vnf.deployment import controller_url
    url = '%s?actor=matterviewer&actor.id=%s&content=html' % (
        controller_url, id)
    link = Link(
        label = label,
        url = url,
        )
    return link


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
