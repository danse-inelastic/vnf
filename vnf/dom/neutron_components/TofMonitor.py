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
class TofMonitor(base):

    name = 'tofmonitors'

    import pyre.db

    tofmin = pyre.db.real( name = 'tofmin', default = 3000 )
    tofmax = pyre.db.real( name = 'tofmax', default = 6000  )
    ntof = pyre.db.integer( name = 'ntof', default = 10 )

    pass # end of TofMonitor


# version
__id__ = "$Id$"

# End of file 
