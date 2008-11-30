#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2008  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.applications.Script import Script as base

class SubmitJob(base):

    class Inventory(base.Inventory):

        import pyre.inventory
        id = pyre.inventory.str('id')

        import pyre.idd
        idd = pyre.inventory.facility('idd-session', factory=pyre.idd.session, args=['idd-session'])
        idd.meta['tip'] = "access to the token server"

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnf.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        dds = pyre.inventory.facility(name="dds", factory=vnf.components.dds)
        dds.meta['tip'] = "the component manages data files"

        csaccessor = pyre.inventory.facility(name='csaccessor', factory = vnf.components.ssher)
        csaccessor.meta['tip'] = 'computing server accessor'

        debug = pyre.inventory.bool(name='debug', default=False)
        pass # end of Inventory
        

    def main(self):
        id = self.id
        job = self.clerk.getJob(id)
        state = job.state
        if state not in ['created', 'submissionfailed']:
            raise RuntimeError, "Job %s not suitable for submission: %s" % (id, state)
        job.state = 'submitting'
        self.clerk.updateRecord(job)

        try:
            computation = job.computation
            if not computation:
                raise RuntimeError, 'computation is not specified for Job: %s' % (id,)
        
            self.prepare(job)
            self.schedule(job)
        except Exception, e:
            job.state = 'submissionfailed'
            errmsg = '%s: %s' % (e.__class__.__name__, e)
            job.error = errmsg
            self.clerk.updateRecord(job)

            import traceback
            self._debug.log('submission of Job %s failed. %s' % (
                id, traceback.format_exc()) )

            if self.debug: raise
            
        return


    def prepare(self, job):
        jobpath = self.dds.abspath(job)
        computation = self.clerk.dereference(job.computation)
        from vnf.components import buildjob
        files, deps = buildjob(computation, db=self.clerk.db, dds=self.dds, path=jobpath)
        for f in files: self.dds.remember(job, f)
        for dep in deps: self.prepare_dependency(dep, job)
        return


    def prepare_dependency(self, dep, job):
        type, id = dep
        record = self.clerk.getRecordByID(type, id)
        self.dds.make_available(record, server=self.clerk.dereference(job.server))
        return


    def schedule(self, job):
        from vnf.components.Scheduler import schedule
        return schedule(job, self)


    def __init__(self, name='submitjob'):
        base.__init__(self, name)
        return


    def _configure(self):
        base._configure(self)
        self._info.log('start _configure')
        self.id = self.inventory.id

        self.debug = self.inventory.debug

        self.idd = self.inventory.idd
        self.clerk = self.inventory.clerk
        self.clerk.director = self
        self.dds = self.inventory.dds
        self.dds.director = self
        self.csaccessor = self.inventory.csaccessor
        self._info.log('end _configure')
        return


    def _init(self):
        base._init(self)

        # initialize table registry
        import vnf.dom
        vnf.dom.register_alltables()

        # set id generator for referenceset
        def _id():
            from vnf.components.misc import new_id
            return new_id(self)
        vnf.dom.set_idgenerator(_id)
        return


    def _getPrivateDepositoryLocations(self):
        return ['../content', '../config']
    

# version
__id__ = "$Id$"

# End of file 
