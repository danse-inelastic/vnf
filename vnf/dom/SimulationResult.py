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


from registry import tableRegistry


from DbObject import DbObject
class SimulationResult(DbObject):

    '''map of "simulation --> result"
    '''

    name = 'simulationresults'

    import pyre.db
    
    simulation = pyre.db.versatileReference( name = 'simulation', tableRegistry = tableRegistry )
    label = pyre.db.varchar( name = 'label', length = 128 )

    pass # end of Block


# version
__id__ = "$Id$"

# End of file 
