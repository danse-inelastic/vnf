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


from pyre.applications.Script import Script as base


class ITaskApp(base):

    from vnf.dom.ITask import ITask as Table

    class Inventory(base.Inventory):

        import pyre.inventory
        id = pyre.inventory.str('id')
        
        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnf.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"
        
        dds = pyre.inventory.facility(name="dds", factory=vnf.components.dds)
        dds.meta['tip'] = "the component manages data files"
        
        csaccessor = pyre.inventory.facility(name='csaccessor', factory = vnf.components.ssher)
        csaccessor.meta['tip'] = 'computing server accessor'
        
        import vnf.inventory
        iworker = vnf.inventory.iworker()
        
        pass # end of Inventory


    def main(self):
        # only if a task was just created, we can start running
        if not self.isCreated():
            task = self.getTask()
            self._debug.log('This task is %s.' % task.state)
            return

        # we must declare the task is running to block future executions
        self.declareRunning()

        # run the real important stuff
        self.iworker.director = self
        try:
            self.iworker.run(self.getTask())
        except:
            import traceback
            tb = traceback.format_exc()
            self._debug.log('Task %s failed: %s' % (self.id, tb))
            task = self.getTask()
            task.error = tb
            task.state = 'failed'
            self.clerk.updateRecord(task)
            return

        # declare that this task finished
        self.declareFinished()
        return


    def declareRunning(self):
        task = self.getTask()
        task.state = 'running'
        self.clerk.updateRecord(task)
        return


    def declareFinished(self):
        task = self.getTask()
        task.state = 'finished'
        self.clerk.updateRecord(task)
        return


    def declareProgress(self, percentage, message):
        task = self.getTask()
        task.progress_percentage = percentage
        task.progress_text = message
        self.clerk.updateRecord(task)
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

        self.clerk = self.inventory.clerk
        self.clerk.director = self
        self.dds = self.inventory.dds
        self.dds.director = self
        self.csaccessor = self.inventory.csaccessor

        self.iworker = self.inventory.iworker
        self._info.log('end _configure')
        return


    def _init(self):
        super(ITaskApp, self)._init()

        # initialize table registry
        import vnf.dom
        vnf.dom.register_alltables()
        return



# version
__id__ = "$Id$"

# End of file 
