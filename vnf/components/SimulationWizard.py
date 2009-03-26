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

from vnf.components.Actor import actionRequireAuthentication, AuthenticationError
from vnf.components.FormActor import FormActor as base


class SimulationWizard(base):
    
    
    class Inventory(base.Inventory):
        
        import pyre.inventory
        
        simType = pyre.inventory.str('simType', default = '')
        #simType.validator = pyre.inventory.choice(['sqe', 'eisf', 'dos',
        #    'diffusionCoefficient', 'meanSquareDisplacement', 'vacfcomputations'])
        simType.meta['tip'] = 'type of calculation'

        #type = pyre.inventory.str('type', default='gulpsimulations')
        
        simId = pyre.inventory.str("simId", default='')
        simId.meta['tip'] = "the unique identifier of the simulation"

        pass # end of Inventory


    def default(self, director):
        return self.start(director)

#    def saveSimulation(self, director):
#        try:
#            page = self._retrievePage(director)
#        except AuthenticationError, err:
#            return err.page
#
#        #nothing need to be done.
#        #just go to the simulation list
#        actor = 'materialsimulation'; routine = 'listall'
#        return director.redirect(actor=actor, routine=routine)
#
#
#    def cancel(self, director):
#        try:
#            page = self._retrievePage(director)
#        except AuthenticationError, err:
#            return err.page 
#
#        simulation = self._getSimulation(director)
#        # remove this simulation
#        if simulation: director.clerk.deleteRecord(simulation)
#        
#        # redirect
#        actor = 'materialsimulation'; routine = 'listall'
#        return director.redirect(actor=actor, routine=routine)


    def createJob(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        if not self._readyForSubmission(director):
            return self._notReadyForSubmissionAlert(director)

        # job
        simId = self.inventory.simId
        simType = self.inventory.simType
        computation = director.clerk.getRecordByID(simType, simId)
        jobref = computation.job

        if not jobref or not jobref.id:
            # create a new job
            from vnf.components.Job import new_job
            job = new_job(director)
            job.computation = computation
            director.clerk.updateRecord(job)
            
            computation.job = job
            director.clerk.updateRecord(computation)
        else:
            job = director.clerk.dereference(jobref)
            
        # redirect to job submission page
        actor = 'job'
        routine = 'view'
        return director.redirect(actor, routine, simId = job.id)


    def submitSimulation(self, director):
        return self.createJob(director)


    def __init__(self, name=None):
        if name is None:
            name = "simulationwizard"
        super(SimulationWizard, self).__init__(name)
        return


    def _wizardname(self, simType, director):
        '''return the name of the wizard for the given simulation simType'''
        # this is a bit weird. the simType is the table name. but usually
        # table name has a 's' at the end, and it is not desirable.
        # the following code takes the table class name.
        table = director.clerk._getTable(simType)
        table = table.__name__.lower()
        
        return '%swizard' % table


    def _createSimulation(self, director, matter=None):

        simType = self.inventory.simType
        Computation = director.clerk._getTable(simType)
        
        computation = director.clerk.newOwnedObject(Computation)
        self.inventory.simId = computation.id
        if matter:
            computation.matter = matter
        director.clerk.updateRecord(computation)
        return computation


    def _readyForSubmission(self, director, matter=None):
        simId = self.inventory.simId
        simType = self.inventory.simType
        if not simId or not simType: return False
        simulation = director.clerk.getRecordByID(simType, simId)
        return True


    def _notReadyForSubmissionAlert(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page
        main = page._body._content._main
        document = main.document(title='Simulation' )
        document.byline = '<a href="http://danse.us">DANSE</a>'    
        p = document.paragraph()
        p.text = [
            'Not yet ready for submission',
            ]
        return page


    def _getSimulation(self, director):
        simId = self.inventory.simId
        table = self.inventory.simType
        if not table or not simId: return
        return director.clerk.getRecordByID(table, simId)

    pass # end of SimulationWizard





# version
__id__ = "$Id$"

# End of file 
