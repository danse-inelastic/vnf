# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from _ import o2t


# data object
# we should use the histogram data object in the histogram package in the long run
class Histogram:

    pass


# orm
from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    dbtablename = 'histograms'

Histogram.Inventory = Inventory


# db table
from ComputationResult import ComputationResult
HistogramTable = o2t(Histogram, {'subclassFrom': ComputationResult})
HistogramTable.datafiles = [
    'data.h5',
    ]



# version
__id__ = "$Id$"

# End of file 
