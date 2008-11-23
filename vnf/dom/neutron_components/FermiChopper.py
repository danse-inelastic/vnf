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
class FermiChopper(base):

    name = 'fermichoppers'

    import pyre.db

    len = pyre.db.real(name='len', default=0.1)
    w = pyre.db.real(name='w', default=0.06)
    ymin = pyre.db.real(name='ymin', default=-.0325)
    ymax = pyre.db.real(name='ymax', default=.0325)
    nu = pyre.db.integer(name='nu', default=600)
    delta = pyre.db.real(name='delta', default=0.0)
    tc = pyre.db.real(name='tc', default=0.0)
    nchans = pyre.db.integer(name='nchans', default=10)
    bw = pyre.db.real(name='bw', default=0.0005)
    blader = pyre.db.real(name='blader', default=0.5)    

    pass # end of FermiChopper


# version
__id__ = "$Id$"

# End of file 
