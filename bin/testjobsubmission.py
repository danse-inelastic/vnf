#!/usr/bin/env python
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


from pyre.applications.Script import Script as base


class TestApp(base):


    class Inventory(base.Inventory):
        
        import pyre.inventory

        # properties
        db = pyre.inventory.str(name='db', default='vnf')
        db.meta['tip'] = "the name of the database"

        dbwrapper = pyre.inventory.str(name='dbwrapper', default='psycopg')
        dbwrapper.meta['tip'] = "the python package that provides access to the database back end"

        # components
        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnf.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        csaccessor = pyre.inventory.facility( name='csaccessor', factory = vnf.components.ssher)
        csaccessor.meta['tip'] = 'computing server accessor'


    def main(self, *args, **kwds):
        # create a new job
        jobid = 'testjob000'
        from vnf.dom.Job import Job
        # delete the record if necessary
        try: self.db.deleteRow(Job, where="id='%s'" % jobid)
        except: pass
        job = Job()
        job.id = jobid
        job.server = 'server000'
        self.clerk.newRecord(job)

        # make this job a dummy job
        from vnf.components.JobDataManager import JobDataManager
        path = JobDataManager(job, self.db).localpath()
        DummyJobBuilder(path).render()

        # schedule the job
        from vnf.components.Scheduler import schedule
        schedule(job, director = self)
        return


    def __init__(self, name):
        base.__init__(self, name)

        # turn on the info channel
        self._info.activate()

        return


    def _configure(self):
        super(TestApp, self)._configure()

        self.clerk = self.inventory.clerk
        self.clerk.director = self
        self.csaccessor = self.inventory.csaccessor
        return


    def _init(self):
        super(TestApp, self)._init()

        # connect to the database
        import pyre.db
        dbkwds = DbAddressResolver().resolve(self.inventory.db)
        self.db = pyre.db.connect(wrapper=self.inventory.dbwrapper, **dbkwds)

        # initialize the accessors
        self.clerk.db = self.db

        # initialize table registry
        import vnf.dom
        vnf.dom.register_alltables()
        return


    def _getPrivateDepositoryLocations(self):
        return ['../config']



from vnf.components.JobBuilder import JobBuilder
class DummyJobBuilder(JobBuilder):

    def render(self, computation = None):
        import os
        #create directory
        if not os.path.exists(self.path): os.makedirs(self.path)
        #create run.sh
        path = os.path.join(self.path, self.shscriptname)
        cmd = 'ls -al'
        open(path, 'w').write( cmd )
        return


from vnf.DbAddressResolver import DbAddressResolver


def main():
    import journal
    journal.debug('curator').activate()

    TestApp('testjobsubmission').run()
    return


if __name__ == '__main__': main()

# version
__id__ = "$Id$"

# End of file 
