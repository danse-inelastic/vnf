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


from NeutronComponent import NeutronComponent as base
class IQMonitor(base):

    name = 'iqmonitors'

    import pyre.db

    Qmin = pyre.db.real( name = 'Qmin', default = 0. )
    Qmax = pyre.db.real( name = 'Qmax', default = 13.  )
    nQ = pyre.db.integer( name = 'nQ', default = 130 )

    pass # end of IQMonitor


# version
__id__ = "$Id$"

# End of file 
