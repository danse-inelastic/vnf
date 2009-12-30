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


#from Monitor import Monitor as base
from AbstractNeutronComponent import AbstractNeutronComponent as base
class NeutronRecorder(base):

    name = 'neutronrecorders'

    import dsaw.db

    packetsize = dsaw.db.integer(name='packetsize', default=10000)

    pass # end of NeutronRecorder


# version
__id__ = "$Id$"

# End of file 
