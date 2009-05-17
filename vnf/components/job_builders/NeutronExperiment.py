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


from JobBuilder import JobBuilder as base
class Builder(base):

    from vnf.dom.NeutronExperiment import NeutronExperiment as Computation

    def render(self, computation, db=None, dds=None):
        from NeutronExperimentSimulationRunBuilder import Builder
        return Builder(self.path).render(computation, db=db, dds=dds)


# the relative path in the job directory where mcvine simulation will
# generate outputs
outputdir = 'out'
outputdirs = [
    outputdir,
    #'out-server-0', # temp hack to deal with parallel simulation
    ]

import os
def outputfilename(component):
    """output file name for the given neutron component
    in the output directory of the job directory
    
    This has to be unique so that different components don't
    write to the same output file.
    """
    f = '%s-%s.out' % (component.__class__.__name__, component.label)
    return f


def outputfiles(component):
    '''paths of output files for the given component
    '''
    from InstrumentSimulationAppBuilder import _ComponentOutputfiles
    ret = []
    for dir in outputdirs:
        ret += _ComponentOutputfiles(dir).dispatch(component)
        continue
    return ret


# version
__id__ = "$Id$"

# End of file 
