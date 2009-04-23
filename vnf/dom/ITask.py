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
    progress_text = pyre.db.varchar(name='progress_text', length=1024)

    # the party that benefits from this internal task
    beneficiary = pyre.db.versatileReference(
        name = 'beneficiary', tableRegistry = tableRegistry)
    
    # the type of this internal task
    type = pyre.db.varchar(name='type', length=32)

    # the worker of this internal task
    worker = pyre.db.varchar(name='worker', length=32)
    
    options = pyre.db.varcharArray(name='options', length=64, default=[])

    error = pyre.db.varchar(name='error', length=1024)


def createITask(id, beneficiary, worker, type='', state='created', **options):
    t = ITask()
    t.id = id
    t.beneficiary = beneficiary
    t.worker = worker
    opts = []
    for k, v in options.iteritems():
        opts.append(str(k))
        opts.append(str(v))
        continue
    t.options = opts
    t.type = type
    t.state = state
    t.progress_percentage = 0
    return t


def inittable(db):
    def r(id):
        r = ITask()
        r.id = id
        return r
    
    records = [
        r('test-itask'), # just for test
        ]
    
    for r in records: db.insertRow( r )
    return


def initids():
    return [
        'test-itask', 
        ]




# version
__id__ = "$Id$"

# End of file 
