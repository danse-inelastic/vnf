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


from registry import tableRegistry

analysisClasses = ['Sqe','Eisf','Dos','DiffusionCoefficient',
                       'MeanSquareDisplacement','VelocityAutocorrelation']

from Computation import Computation as base
class Analysis(base):

    # future base class for all analysis computations
    pass
    


# version
__id__ = "$Id$"

# End of file 
