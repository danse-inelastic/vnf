# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



from registry import tableRegistry

from DbObject import DbObject as base
class SampleComponentExample(base):

    # Examples of sample components. Records of this table will serve
    # as templates and user can start from these templates and build
    # sample components by modifying its parameters.

    name = 'samplecomponentexamples'

    import dsaw.db

    samplecomponent = dsaw.db.versatileReference(
        name = 'samplecomponent')

    pass # end of SampleComponentExample


def inittable(db):
    def new( id, samplecomponent):
        r = SampleComponentExample()
        r.id = id
        r.samplecomponent = samplecomponent
        return r

    records = [
        new('vanadiumplate-000001: samplecomp example 1',
            'vanadiumplates###vanadiumplate-000001'),
        ]
    
    for r in records: db.insertRow( r )
    return


def initids():
    return [
        'vanadiumplate-000001: samplecomp example 1',
        ]

# version
__id__ = "$Id$"

# End of file 
