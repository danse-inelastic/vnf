# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from SampleComponent import SampleComponent as base
class VanadiumPlate(base):

    name = 'vanadiumplates'

    import dsaw.db

    # dimensions (unit: meter)
    width = dsaw.db.real(name='width', default=0.05)
    height = dsaw.db.real(name='height', default=0.10)
    thickness = dsaw.db.real(name='thickness', default=0.002)

    # target definition
    target_radius = dsaw.db.real(name='target_radius', default=0)
    target_radius.meta['tip'] = 'radius of disk containg target. use 0 for full space'
    
    target_position = dsaw.db.doubleArray(name='target_position', default=(0,0,0))
    
    pass # end of Vanadiumplates


def inittable(db):
    Table = VanadiumPlate
    def new(id, short_description, width, height, thickness, target_radius, target_position):
        r = Table()
        r.id = id
        r.short_description = short_description
        r.width = width
        r.height = height
        r.thickness = thickness
        r.target_radius = target_radius
        r.target_position = target_position
        return r
    records = [
        new('vanadiumplate-000001', 'Vanadium plate',
            0.05, 0.10, 0.002, 0, (0,0,0)),
        ]
    for r in records: db.insertRow( r )
    return


def initids():
    return [
        'vanadiumplate-000001',
        ]


# version
__id__ = "$Id$"

# End of file 
