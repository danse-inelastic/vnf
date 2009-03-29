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

# eventually generalize this to other types of md
from vnf.dom.GulpSimulation import GulpSimulation

#from Analysis import Analysis as base
from vnf.dom.Computation import Computation

class VacfComputation(Computation):

    name = 'vacfcomputations'

    import pyre.db as d

    units = d.varchar(name='units', length = 16, default = 'nm') # unit meV
    weights = d.varchar(name='weights', length = 16, default = 'mass') # number of sampling points (in 1 dimension)

    gulpsimulation = d.reference(name='gulpsimulation', table = GulpSimulation)
    
#    # the trajectory name can be either a  file name or an id
#    from vnf.dom.Trajectory import Trajectory
#    trajectory = pyre.db.reference(name='trajectory', table=Trajectory)

# version
__id__ = "$Id$"

# End of file 
