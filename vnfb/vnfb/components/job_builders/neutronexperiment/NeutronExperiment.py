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


from _ import JobBuilder as base

class Builder(base):

    from vnfb.dom.neutron_experiment_simulations.NeutronExperiment import NeutronExperiment as Computation

    def render(self, computation, db=None, dds=None):
        # make sure orm is initd
        domaccess = self.director.retrieveDOMAccessor('experiment')
        orm = domaccess.orm

        # convert db record to data object
        # computation = orm.record2object(computation)
        
        #
        from NeutronExperimentSimulationRunBuilder import Builder
        builder = Builder(self.path)
        builder.director = self.director
        return builder.render(computation, db=db, dds=dds)


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
    f = '%s-%s.out' % (component.__class__.__name__, component.componentname)
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
