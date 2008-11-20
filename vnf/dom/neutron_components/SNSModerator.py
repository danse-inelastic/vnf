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
    dist = pyre.db.integer(name='dist', default=2.5)
    xw = pyre.db.integer(name='xw', default=0.1)
    yh = pyre.db.integer(name='yh', default=0.1)
    Emin = pyre.db.integer(name='Emin', default=0)
    Emax = pyre.db.integer(name='Emax', default=100)

    pass # end of SNSModerator


# version
__id__ = "$Id$"

# End of file 
