# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from registry import tableRegistry

from OwnedObject import OwnedObject as base
class ITask(base):

    'internal tasks'

    name = 'itasks'

    import pyre.db
    
    time_completion = pyre.db.timestamp(name='time_completion')
    time_completion.meta['tip'] = 'time left to completion'
    
    time_start = pyre.db.timestamp(name='time_start')
    time_start.meta['tip'] = 'the time the job started'
    
    state = pyre.db.varchar( name = 'state', length = 16 )
    # state:
    #   - created: just created. has not been submitted
    #   - running
    #   - finished
    #   - failed
    #   - cancelled
    
    progress_percentage = pyre.db.real(name='progress_percentage')
    progress_text = pyre.db.varchar(name='progress_text', length=32)

    type = pyre.db.varchar(name='type', length=32)
    worker = pyre.db.varchar(name='worker', length=32)
    
    cmdoptions = pyre.db.varchar(name='cmdoptions', length=256)

    error = pyre.db.varchar(name='error', length=1024)


# version
__id__ = "$Id$"

# End of file 
