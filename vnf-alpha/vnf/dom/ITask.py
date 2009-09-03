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

    import dsaw.db
    
    time_completion = dsaw.db.timestamp(name='time_completion')
    time_completion.meta['tip'] = 'time left to completion'
    
    time_start = dsaw.db.timestamp(name='time_start')
    time_start.meta['tip'] = 'the time the job started'
    
    state = dsaw.db.varchar( name = 'state', length = 16 )
    # state:
    #   - created: just created. has not been submitted
    #   - running
    #   - finished
    #   - failed
    #   - cancelled
    
    progress_percentage = dsaw.db.real(name='progress_percentage')
    progress_text = dsaw.db.varchar(name='progress_text', length=1024)

    # the party that benefits from this internal task
    beneficiary = dsaw.db.versatileReference(
        name = 'beneficiary')
    
    # the type of this internal task
    type = dsaw.db.varchar(name='type', length=128)

    # the worker of this internal task
    worker = dsaw.db.varchar(name='worker', length=128)
    
    options = dsaw.db.varcharArray(name='options', length=64, default=[])

    error = dsaw.db.varchar(name='error', length=8192)


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
