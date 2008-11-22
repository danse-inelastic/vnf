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
class SNSModerator(base):

    name = 'snsmoderators'

    import pyre.db

    width = pyre.db.real(name='width', default=0.1)
    height = pyre.db.real(name='height', default=0.1)
    dist = pyre.db.real(name='dist', default=2.5)
    xw = pyre.db.real(name='xw', default=0.1)
    yh = pyre.db.real(name='yh', default=0.1)
    Emin = pyre.db.real(name='Emin', default=0)
    Emax = pyre.db.real(name='Emax', default=100)

    pass # end of SNSModerator


# version
__id__ = "$Id$"

# End of file 
