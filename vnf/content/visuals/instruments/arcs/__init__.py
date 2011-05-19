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


def beamprofile(director=None, name=None, actor=None):
    if director is None:
        raise RuntimeError, "director cannot be none"
    name = name or "beam-profile"
    actor = actor or "instruments/arcs/beam-profile"
    from BeamProfile import BeamProfile
    return BeamProfile(director=director, name=name, actor=actor)


def iqeresolution(director=None, name=None, actor=None):
    if director is None:
        raise RuntimeError, "director cannot be none"
    name = name or "iqe-resolution"
    actor = actor or "instruments/arcs/iqe-resolution"
    from IQEResolutionComputation import IQEResolutionComputation
    return IQEResolutionComputation(director=director, name=name, actor=actor)


# version
__id__ = "$Id$"

# End of file 
