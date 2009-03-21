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
from vnf.dom.Computation import Computation as base

class VacfComputation(base):

    name = 'vacfcomputations'

    import pyre.db
    # the trajectory name can be either a  file name or an id
    from vnf.dom.Trajectory import Trajectory
    trajectory = pyre.db.reference(name='trajectory', table=Trajectory)
    units = pyre.db.varchar(name='units', length = 16, default = 'nm') # unit meV
    weights = pyre.db.varchar(name='weights', length = 16, default = 'mass') # number of sampling points (in 1 dimension)

    gulpsimulation = pyre.db.reference(name='gulpsimulation', table = GulpSimulation)


# version
__id__ = "$Id$"

# End of file 
