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


from Monitor import Monitor as base
class QEMonitor(base):

    name = 'qemonitors'

    import dsaw.db

    Emin = dsaw.db.real( name = 'Emin', default = -50. )
    Emax = dsaw.db.real( name = 'Emax', default = 50. )
    nE = dsaw.db.integer( name = 'nE', default = 100)

    Qmin = dsaw.db.real( name = 'Qmin', default = 0. )
    Qmax = dsaw.db.real( name = 'Qmax', default = 13.  )
    nQ = dsaw.db.integer( name = 'nQ', default = 130 )

    max_angle_in_plane = dsaw.db.real(
        name = 'max_angle_in_plane', default = 120. )
    min_angle_in_plane = dsaw.db.real(
        name = 'min_angle_in_plane', default = -30 )
    max_angle_out_of_plane = dsaw.db.real(
        name = 'max_angle_out_of_plane', default = 30 )
    min_angle_out_of_plane = dsaw.db.real(
        name = 'min_angle_out_of_plane', default = -30 )
    
    pass # end of QEMonitor


# version
__id__ = "$Id$"

# End of file 
