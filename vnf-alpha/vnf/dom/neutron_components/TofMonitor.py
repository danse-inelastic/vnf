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
class TofMonitor(base):

    name = 'tofmonitors'

    import pyre.db

    tmin = pyre.db.real( name = 'tmin', default = 3000e-6 )
    tmax = pyre.db.real( name = 'tmax', default = 6000e-6  )
    x_min = pyre.db.real( name = 'x_min', default = -0.1 )
    x_max = pyre.db.real( name = 'x_max', default = 0.1 )
    y_min = pyre.db.real( name = 'y_min', default = -0.1 )
    y_max = pyre.db.real( name = 'y_max', default = 0.1 )
    
    nchan = pyre.db.integer( name = 'nchan', default = 100 )

    pass # end of TofMonitor


# version
__id__ = "$Id$"

# End of file 
