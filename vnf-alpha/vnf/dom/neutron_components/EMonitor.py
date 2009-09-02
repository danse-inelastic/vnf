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

    import pyre.db

    Emin = pyre.db.real( name = 'Emin', default = 10 )
    Emax = pyre.db.real( name = 'Emax', default = 100 )
    x_min = pyre.db.real( name = 'x_min', default = -0.1 )
    x_max = pyre.db.real( name = 'x_max', default = 0.1 )
    y_min = pyre.db.real( name = 'y_min', default = -0.1 )
    y_max = pyre.db.real( name = 'y_max', default = 0.1 )
    
    nchan = pyre.db.integer( name = 'nchan', default = 100 )
    
    pass # end of EMonitor


# version
__id__ = "$Id$"

# End of file 
