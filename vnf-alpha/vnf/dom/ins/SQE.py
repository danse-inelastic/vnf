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


from ComputationResult import ComputationResult as base
class SQE(base):

    name = 'sqes'

    histogramh5 = 'sqe.h5'
    datafiles = [
        histogramh5,
        ]
    
    pass # end of SQE


# version
__id__ = "$Id$"

# End of file 
