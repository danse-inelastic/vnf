#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2009  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from luban.applications.UIApp import UIApp as base


class ITaskApp(base):

    from vnf.dom.ITask import ITask as Table

    class Inventory(base.Inventory):

        import pyre.inventory
        id = pyre.inventory.str('id')
        
        import pyre.idd
        idd = pyre.inventory.facility('idd-session', factory=pyre.idd.session, args=['idd-session'])
        idd.meta['tip'] = "access to the token server"

        clerk = pyre.inventory.facility(name="clerk", default='clerk')
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"
        
        import vnfb.components
        import vnf.components
        dds = pyre.inventory.facility(name="dds", factory=vnfb.components.dds)
        dds.meta['tip'] = "the component manages data files"
        
        csaccessor = pyre.inventory.facility(name='csaccessor', factory = vnf.components.ssher)
        csaccessor.meta['tip'] = 'computing server accessor'
        
        import vnf.inventory
        iworker = vnf.inventory.iworker()
        
        pass # end of Inventory


    def main(self):
        task = self.getTask()
        
        # only if a task was just created, we can start running
        if not self.isCreated():
            self._debug.log('This task is %s.' % task.state)
            return

        # we must declare the task is running to block future executions
        self.declareRunning()

        # run the real important stuff
        self.iworker.director = self
        try:
            self.iworker.run(task)
        except:
            import traceback 

            tb = traceback.format_exc()
            self._debug.log('Task %s failed: %s' % (self.id, tb))

            tb = tb[:task.__class__.error.length]
            task.error = tb
            task.state = 'failed'
            try:
                self.clerk.updateRecordWithID(task)
            except:
                import traceback
                tb = traceback.format_exc()
                self._debug.log("Failed to update task %s.\n%s" % (self.id, tb))
            return

        # declare that this task finished
        self.declareFinished()
        return


    def declareRunning(self):
        task = self.getTask()
        task.state = 'running'
        self.clerk.updateRecordWithID(task)
        return


    def declareFinished(self):
        task = self.getTask()
        task.state = 'finished'
        self.clerk.updateRecordWithID(task)
        return


    def declareProgress(self, fractional=None, message=None, percentage=None):
        if fractional is not None and percentage is not None:
            raise RuntimeError, "both fractional and percentage are supplied"
        if fractional is not None: percentage = fractional * 100

        self._debug.log('%s: %s' % (percentage, message))
        task = self.getTask()
        task.progress_percentage = percentage
        task.progress_text = message
        self.clerk.updateRecordWithID(task)
        return task


    def isCreated(self):
        task = self.getTask()
        return task.state == 'created'
    
        
    def isFinished(self):
        task = self.getTask()
        return task.state == 'finished'
    
        
    def getTask(self):
        return self.clerk.getRecordByID(self.Table, self.id)


    def __init__(self, name=None):
        if name is None:
            name='itaskapp'
        super(ITaskApp, self).__init__( name)
        return


    def _configure(self):
        super(ITaskApp, self)._configure()
        self._info.log('start _configure')
        self.id = self.inventory.id

        self.idd = self.inventory.idd
        self.clerk = self.inventory.clerk
        self.clerk.director = self
        self.dds = self.inventory.dds
        self.dds.director = self
        self.csaccessor = self.inventory.csaccessor

        self.iworker = self.inventory.iworker
        if self.iworker.__class__.__name__ == 'Dummy':
            dump = self._dumpCurator()
            raise RuntimeError, 'iworker is not implemented right.\n%s' % dump
        self._info.log('end _configure')
        return


    def _init(self):
        super(ITaskApp, self)._init()
        return



# version
__id__ = "$Id$"

# End of file 
