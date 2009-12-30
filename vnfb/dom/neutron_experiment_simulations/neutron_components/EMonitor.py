# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2007-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Monitor import Monitor as base
class EMonitor(base):

    name = 'emonitors'

    import dsaw.db

    Emin = dsaw.db.real( name = 'Emin', default = 10 )
    Emax = dsaw.db.real( name = 'Emax', default = 100 )
    x_min = dsaw.db.real( name = 'x_min', default = -0.1 )
    x_max = dsaw.db.real( name = 'x_max', default = 0.1 )
    y_min = dsaw.db.real( name = 'y_min', default = -0.1 )
    y_max = dsaw.db.real( name = 'y_max', default = 0.1 )
    
    nchan = dsaw.db.integer( name = 'nchan', default = 100 )
    
    pass # end of EMonitor


# version
__id__ = "$Id$"

# End of file 
