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

        db = pyre.inventory.str(name='db', default='vnf')
        db.meta['tip'] = "the name of the database"

        dbwrapper = pyre.inventory.str(name='dbwrapper', default='psycopg')
        dbwrapper.meta['tip'] = "the python package that provides access to the database back end"

        import pyre.idd
        idd = pyre.inventory.facility('idd-session', factory=pyre.idd.session, args=['idd-session'])
        idd.meta['tip'] = "access to the token server"

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnf.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        dds = pyre.inventory.facility(name="dds", factory=vnf.components.dds)
        dds.meta['tip'] = "the component manages data files"

        csaccessor = pyre.inventory.facility( name='csaccessor', factory = vnf.components.ssher)
        csaccessor.meta['tip'] = 'computing server accessor'

        pass # end of Inventory
        

    def main(self):
        id = self.id
        job = self.clerk.getJob(id)
        state = job.state
        if state not in ['created']:
            raise RuntimeError, "Job %s not suitable for submission: %s" % (id, state)
        computation = job.computation
        if not computation:
            raise RuntimeError, 'computation is not specified for Job: %s' % (id,)
        self.prepare(job)
        self.schedule(job)
        return


    def prepare(self, job):
        jobpath = self.dds.abspath(job)
        computation = job.computation.dereference(self.db)
        from vnf.components import buildjob
        files = buildjob(computation, db=self.db, dds=self.dds, path=jobpath)
        for f in files: self.dds.remember(job, f)
        return


    def schedule(self, job):
        from vnf.components.Scheduler import schedule
        return schedule(job, self)


    def __init__(self, name='submitjob'):
        base.__init__(self, name)
        return


    def _configure(self):
        base._configure(self)
        self.id = self.inventory.id

        self.idd = self.inventory.idd
        self.clerk = self.inventory.clerk
        self.clerk.director = self
        self.dds = self.inventory.dds
        self.dds.director = self
        self.csaccessor = self.inventory.csaccessor
        return


    def _init(self):
        base._init(self)

        import sys
        self._debug.log('sys.path=%s' % (sys.path,))
        import os
        self._debug.log('os.environ=%s' % (os.environ,))

        # connect to the database
        import pyre.db
        dbkwds = DbAddressResolver().resolve(self.inventory.db)
        self.db = pyre.db.connect(wrapper=self.inventory.dbwrapper, **dbkwds)

        # initialize the accessors
        self.clerk.db = self.db

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
    

from vnf.DbAddressResolver import DbAddressResolver


# version
__id__ = "$Id$"

# End of file 
