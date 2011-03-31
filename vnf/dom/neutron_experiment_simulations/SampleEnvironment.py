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


class SampleEnvironment(object):

    #unit: K
    temperature = 300.

    #unit: Tesla
    magnetic_field = [0.,0.,0.]

    #unit: atm
    pressure = 1.
    

from _ import o2t
SampleEnvironmentTable = o2t(SampleEnvironment)


# version
__id__ = "$Id$"

# End of file 
