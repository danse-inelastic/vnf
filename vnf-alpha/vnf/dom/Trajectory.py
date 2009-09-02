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


from OwnedObject import OwnedObject as base
class Trajectory(base):
    # class for md trajectories
    import pyre.db

    #creator = pyre.db.reference(name='creator', table = User)

    
    timespan = pyre.db.real(name='timespan')
    timespan.meta['tip'] = 'timespan of trajectory'
    
    pass
    


# version
__id__ = "$Id$"

# End of file 
