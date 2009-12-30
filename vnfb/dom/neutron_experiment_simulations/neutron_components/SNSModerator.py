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


from SNSModeratorMCSimulatedData import SNSModeratorMCSimulatedData

from AbstractNeutronComponent import AbstractNeutronComponent as base
class SNSModerator(base):

    name = 'snsmoderators'

    import dsaw.db

    width = dsaw.db.real(name='width', default=0.1)
    height = dsaw.db.real(name='height', default=0.1)
    dist = dsaw.db.real(name='dist', default=2.5)
    xw = dsaw.db.real(name='xw', default=0.1)
    yh = dsaw.db.real(name='yh', default=0.1)
    Emin = dsaw.db.real(name='Emin', default=0)
    Emax = dsaw.db.real(name='Emax', default=100)
    neutronprofile = dsaw.db.reference(name='neutronprofile', table=SNSModeratorMCSimulatedData)

    pass # end of SNSModerator


# version
__id__ = "$Id$"

# End of file 
