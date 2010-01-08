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

    radius = 3.
    ncolumns = 100
    nrows = 100
    
    pass


InvBase=base.Inventory
class Inventory(InvBase):

    radius = InvBase.d.float( name = 'radius', default = 3., validator=InvBase.v.positive )
    ncolumns = InvBase.d.int( name = 'ncolumns', default = 100, validator=InvBase.v.positive)
    nrows = InvBase.d.int( name = 'nrows', default = 100, validator=InvBase.v.positive)
    
    dbtablename = 'sphericalpsds'



SphericalPSD.Inventory = Inventory
del Inventory


from _ import o2t, MonitorTableBase
SphericalPSDTable = o2t(SphericalPSD, {'subclassFrom': MonitorTableBase})


# version
__id__ = "$Id$"

# End of file 
