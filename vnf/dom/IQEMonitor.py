# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from OwnedObject import OwnedObject
class IQEMonitor(OwnedObject):

    name = 'iqemonitors'

    import pyre.db

    Emin = pyre.db.real( name = 'Emin', default = -50. )
    Emax = pyre.db.real( name = 'Emax', default = 50. )
    nE = pyre.db.integer( name = 'nE', default = 100)

    Qmin = pyre.db.real( name = 'Qmin', default = 0. )
    Qmax = pyre.db.real( name = 'Qmax', default = 13.  )
    nQ = pyre.db.integer( name = 'nQ', default = 130 )

    max_angle_in_plane = pyre.db.real(
        name = 'max_angle_in_plane', default = 120. )
    min_angle_in_plane = pyre.db.real(
        name = 'min_angle_in_plane', default = -30 )
    max_angle_out_of_plane = pyre.db.real(
        name = 'max_angle_out_of_plane', default = 30 )
    min_angle_out_of_plane = pyre.db.real(
        name = 'min_angle_out_of_plane', default = -30 )
    
    pass # end of IQEMonitor


# version
__id__ = "$Id$"

# End of file 
