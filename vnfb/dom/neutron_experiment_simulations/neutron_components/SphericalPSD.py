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


from Monitor import Monitor as base
class SphericalPSD(base):

    pass


InvBase=base.Inventory
class Inventory(InvBase):

    radius = InvBase.d.float( name = 'radius', default = 3., validator=InvBase.v.positive )
    ncolumns = InvBase.d.int( name = 'ncolumns', default = 100, validator=InvBase.v.positive)
    nrows = InvBase.d.int( name = 'nrows', default = 100, validator=InvBase.v.positive)
    
    dbtablename = 'sphericalpsds'



SphericalPSD.Inventory = Inventory
del Inventory


from _ import o2t
SphericalPSDTable = o2t(SphericalPSD)


# version
__id__ = "$Id$"

# End of file 
