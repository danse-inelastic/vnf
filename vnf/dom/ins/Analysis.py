# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

analysisClasses = ['Sqe','Eisf','Dos','DiffusionCoefficient',
                       'MeanSquareDisplacement','VelocityAutocorrelation']

from vnf.dom.Computation import Computation as base
class Analysis(base):

    # future base class for all analysis computations
    pass
    


# version
__id__ = "$Id$"

# End of file 
