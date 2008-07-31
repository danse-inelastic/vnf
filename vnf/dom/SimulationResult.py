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


from DbObject import DbObject
class SimulationResult(DbObject):

    '''map of "simulation --> result"
    '''

    name = 'simulationresults'

    import pyre.db

    simulation_type = pyre.db.varchar( name = 'simulation_type', default = 'NeutronExperiment', length = 128 )
    simulation_id = pyre.db.varchar( name = 'simulation_id', length = 100 )

    label = pyre.db.varchar( name = 'label', length = 128 )

    pass # end of Block


# version
__id__ = "$Id$"

# End of file 
