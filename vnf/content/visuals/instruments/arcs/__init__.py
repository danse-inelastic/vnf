# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


"""
this subpackage is for visuals of  applications of arcs instrument.
These applications are for data reduction, analysis, and
simulations of arcs.
Please note this is different from ..neutron_experiments 
-- ..neutron_experiments is for generic instrument simulations of
   experiments.
"""


def beamprofile(**kwds):
    from BeamProfile import BeamProfile
    return BeamProfile(**kwds)


def iqeresolution(**kwds):
    from IQEResolutionComputation import IQEResolutionComputation
    return IQEResolutionComputation(**kwds)


# version
__id__ = "$Id$"

# End of file 
