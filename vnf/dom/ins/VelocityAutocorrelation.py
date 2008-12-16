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

from Analysis import Analysis as base

class VelocityAutocorrelation(base):

    name = 'velocityautocorrelations'

    import pyre.db
    # the trajectory name can be either a  file name or an id
    trajectoryName = pyre.db.varchar(name='trajectoryName', length = 128)
    units = pyre.db.varchar(name='units', length = 16, default = 'nm') # unit meV
    weights = pyre.db.varchar(name='weights', length = 16, default = 'mass') # number of sampling points (in 1 dimension)




# version
__id__ = "$Id$"

# End of file 
