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
class QMonitor(base):

    name = 'qmonitors'

    import dsaw.db

    Qmin = dsaw.db.real( name = 'Qmin', default = 0. )
    Qmax = dsaw.db.real( name = 'Qmax', default = 13.  )
    nQ = dsaw.db.integer( name = 'nQ', default = 130 )

    pass # end of QMonitor


# version
__id__ = "$Id$"

# End of file 
