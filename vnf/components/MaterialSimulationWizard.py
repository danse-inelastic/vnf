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


from Actor import actionRequireAuthentication, action_link, AuthenticationError
from FormActor import FormActor as base, InputProcessingError


class MaterialSimulationWizard(base):
    
    
    class Inventory(base.Inventory):
        
        import pyre.inventory

        type = pyre.inventory.str('type', default='gulpsimulations')
        
        id = pyre.inventory.str("id", default='')
        id.meta['tip'] = "the unique identifier of the material simulation"

        matterid = pyre.inventory.str('matterid')
        mattertype = pyre.inventory.str('mattertype')

        pass # end of Inventory


    def default(self, director):
        return self.start(director)

    def start(self, director):
        return self.selectMaterial(director)
    

    def selectMaterial(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        # find out the previously selected material
        id = self.inventory.id
        type = self.inventory.type
        if id and type:
            simulation = director.clerk.getRecordByID(type, id)
            matter = simulation.matter
            selected = str(matter)
        else:
            selected = ''

        main = page._body._content._main

        # populate the main column
        document = main.document(title='Material Simulation/Modeling Wizard: select material')
        document.description = ''
        document.byline = 'byline?'

        formcomponent = self.retrieveFormToShow(
            'selectmaterial' )
        formcomponent.director = director
        formcomponent.inventory.selected = selected
        
        # create form
        form = document.form(
            name='selectmaterial',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'materialsimulationwizard', sentry = director.sentry,
            label = '', routine = 'verifyMaterialSelection',
            id = self.inventory.id, type = self.inventory.type,
            arguments = {'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        # run button
        submit = form.control(
            name="actor.form-received.submit", type="submit", value="Continue")

        return page
    

    def verifyMaterialSelection(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        mattertype,matterid = self.processFormInputs(director)
        self.inventory.matterid = matterid
        self.inventory.mattertype = mattertype
        
        return self.selectSimulationEngine(director)


    def selectSimulationEngine(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        # if simulation already created, don't need to select simulation type
        # again. just jump to configure
        if self.inventory.id:
            return self.configureSimulation(director)
        
        main = page._body._content._main
        # populate the main column
        document = main.document(
            title='Select material simulation/modeling engine')
        document.description = ''
        document.byline = '<a href="http://danse.us">DANSE</a>'        

        mattertype = self.inventory.mattertype
        matterid = self.inventory.matterid
        if not matterid or not mattertype:
            p = document.paragraph()
            p.text = [
                'You have not selected the material.',
                ]
            return page
            
        formcomponent = self.retrieveFormToShow( 'selectSimulationEngine')
        formcomponent.director = director
        formcomponent.inventory.type = self.inventory.type
        
        # build the form 
        form = document.form(name='', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'materialsimulationwizard', 
            sentry = director.sentry,
            routine = 'verifySimulationTypeSelection',
            id=self.inventory.id,
            type=self.inventory.type,
            matterid = self.inventory.matterid,
            mattertype = self.inventory.mattertype,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        submit = form.control(name='submit',type="submit", value="Continue")
        #self.processFormInputs(director)
        return page    
    

    def verifySimulationTypeSelection(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        self.inventory.type = type = self.processFormInputs(director)

        # create a new simulation
        mattertype = self.inventory.mattertype
        matterid = self.inventory.matterid
        matter = director.clerk.getRecordByID(mattertype, matterid)
        simulation = self._createSimulation(director, matter=matter)

        # this is a bit weird. the type is the table name. but usually
        # table name has a 's' at the end, and it is not desirable.
        # the following code takes the table class name.
        table = director.clerk._getTable(type)
        table = table.__name__.lower()
        
        actor = '%swizard' % table
        routine = 'configureSimulation'
        return self.redirect(director, actor, routine, simulation = simulation)



    def configureSimulation(self, director):
        raise NotImplementedError


    def saveSimulation(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        #nothing need to be done.
        #just go to the simulation list
        actor = 'materialsimulation'; routine = 'listall'
        return self.redirect(director, actor=actor, routine=routine)


    def cancel(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page 

        simulation = self._getSimulation(director)
        # remove this simulation
        if simulation: director.clerk.deleteRecord(simulation)
        
        # redirect
        actor = 'materialsimulation'; routine = 'listall'
        return self.redirect(director, actor=actor, routine=routine)


    def createJob(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        if not self._readyForSubmission(director):
            return self._notReadyForSubmissionAlert(director)

        # job
        id = self.inventory.id
        type = self.inventory.type
        computation = director.clerk.getRecordByID(type, id)
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
        return self.redirect(director, actor, routine, id = job.id)


    def submitSimulation(self, director):
        return self.createJob(director)


    def __init__(self, name=None):
        if name is None:
            name = "materialsimulationwizard"
        super(MaterialSimulationWizard, self).__init__(name)
        return


    def _createSimulation(self, director, matter=None):
        if not matter:
            raise RuntimeError

        type = self.inventory.type
        Computation = director.clerk._getTable(type)
        
        computation = director.clerk.newOwnedObject(Computation)
        self.inventory.id = id = computation.id
        computation.matter = matter
        director.clerk.updateRecord(computation)
        return computation


    def _readyForSubmission(self, director):
        id = self.inventory.id
        type = self.inventory.type
        if not id or not type: return False
        simulation = director.clerk.getRecordByID(type, id)

        if not simulation.matter: return False
        if not simulation.matter.id: return False
        return True


    def _notReadyForSubmissionAlert(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page
        main = page._body._content._main
        document = main.document(title='Material simulation' )
        document.byline = '<a href="http://danse.us">DANSE</a>'    
        p = document.paragraph()
        p.text = [
            'Not yet ready for submission',
            ]
        return page


    def _materialDefinedForSimulation(self, simulation, director):
        return _materialDefinedForSimulation(simulation, director)


    def _needMaterialAlert(self, director):
        try:
            page = director._retrievePage(director)
        except AuthenticationError, err:
            return err.page
        main = page._body._content._main
        document = main.document(title='Ab initio electronic structure simulation' )
        document.byline = '<a href="http://danse.us">DANSE</a>'    
        p = document.paragraph()
        p.text = [
            'You have not selected the material.',
            ]
        return page


    def _getSimulation(self, director):
        id = self.inventory.id
        type = self.inventory.type
        if not type or not id: return
        return director.clerk.getRecordByID(type, id)


    def _retrievePage(self, director):
        return director.retrieveSecurePage('materialsimulationwizard')


    pass # end of MaterialSimulationWizard



def _materialDefinedForSimulation(simulation, director):
    '''check if a simulation has a valid reference to a material'''
    matter = simulation.matter
    if not matter.table or not matter.id: return False
    try:
        director.clerk.dereference(matter)
    except:
        return False
    return True



from misc import new_id, empty_id, nullpointer

# version
__id__ = "$Id$"

# End of file 
