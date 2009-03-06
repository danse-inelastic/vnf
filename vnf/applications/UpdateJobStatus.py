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


from pyre.applications.Script import Script


class UpdateJobStatus(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnf.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        from vnf.components import dds
        dds = pyre.inventory.facility(name="dds", factory=dds)
        dds.meta['tip'] = "the component manages data files"

        from vnf.components.SSHer import SSHer
        csaccessor = pyre.inventory.facility(
            name='csaccessor', factory = SSHer, args = ['jsu-ssher', 'ssher'])
        csaccessor.meta['tip'] = 'computing server accessor'


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
        
        self.clerk = self.inventory.clerk
        self.clerk.director = self
        
        self.dds = self.inventory.dds
        self.dds.director = self

        self.csaccessor = self.inventory.csaccessor
        return


    def _init(self):
        super(UpdateJobStatus, self)._init()

        # initialize table registry
        import vnf.dom
        vnf.dom.register_alltables()

        return
    

    def _check(self):
        where = "state='submitted' or state='running' or state='onhold'"
        jobs = self.clerk.indexJobs(where=where)
        
        from vnf.components.Scheduler import check
        for job in jobs.itervalues():
            check(job, self)
            continue
        return



# version
__id__ = "$Id$"

# End of file 
