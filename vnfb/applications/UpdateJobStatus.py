#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from luban.applications.UIApp import UIApp as base


class UpdateJobStatus(base):


    class Inventory(base.Inventory):

        import pyre.inventory


    def main(self, *args, **kwds):
        self._check()
        return


    def __init__(self, name=None):
        if name is None:
            name = "updatejobstatus"

        super(UpdateJobStatus, self).__init__(name)
        return


    def _configure(self):
        super(UpdateJobStatus, self)._configure()
        
        logdir = self.inventory.logdir
        today = str(datetime.date.today())
        filename = '%s-update-job-status.log' % today
        logfile = os.path.join(logdir, filename)
        self.ostream = open(logfile, 'a')
        return


    def _check(self):
        self.ostream.write('\n')
        now = str(datetime.datetime.now())
        self.ostream.write('Updating job status: started at %s\n' % now)
        
        where = "state='submitted' or state='running' or state='onhold'"
        domaccess = self.retrieveDOMAccessor('job')
        jobs = domaccess.getJobRecords(filter=where)
        
        from vnfb.utils.job import check
        for job in jobs:
            self.ostream.write('Checking job %s\n' % job.id)
            self.ostream.write(' - before chechking, status=%s\n' % job.state)
            try:
                check(job, self)
            except:
                import traceback
                self.ostream.write(' - **** error in checking **** \m')
                self.ostream.write(traceback.format_exc())
                self.ostream.write(' - *************************** \m')
            self.ostream.write(' - after checking, status=%s\n' % job.state)
            continue
        return


import os, datetime

# version
__id__ = "$Id$"

# End of file 
