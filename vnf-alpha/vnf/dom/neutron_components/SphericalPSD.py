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

    name = 'sphericalpsds'

    import dsaw.db

    radius = dsaw.db.real( name = 'radius', default = 3. )
    ncolumns = dsaw.db.integer( name = 'ncolumns', default = 100 )
    nrows = dsaw.db.integer( name = 'nrows', default = 100 )

    pass # end of TofMonitor


# version
__id__ = "$Id$"

# End of file 
