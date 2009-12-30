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


from AbstractNeutronComponent import AbstractNeutronComponent as base
class FermiChopper(base):

    name = 'fermichoppers'

    import dsaw.db

    len = dsaw.db.real(name='len', default=0.1)
    w = dsaw.db.real(name='w', default=0.06)
    ymin = dsaw.db.real(name='ymin', default=-.0325)
    ymax = dsaw.db.real(name='ymax', default=.0325)
    nu = dsaw.db.integer(name='nu', default=600)
    delta = dsaw.db.real(name='delta', default=0.0)
    tc = dsaw.db.real(name='tc', default=0.0)
    nchans = dsaw.db.integer(name='nchans', default=10)
    bw = dsaw.db.real(name='bw', default=0.0005)
    blader = dsaw.db.real(name='blader', default=0.5)    

    pass # end of FermiChopper


# version
__id__ = "$Id$"

# End of file 
