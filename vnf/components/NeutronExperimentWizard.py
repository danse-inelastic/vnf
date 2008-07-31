#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Actor import actionRequireAuthentication, action_link, AuthenticationError
from FormActor import FormActor as base, InputProcessingError


class NeutronExperimentWizard(base):
    
    
    class Inventory(base.Inventory):
        
        import pyre.inventory
        
        id = pyre.inventory.str("id", default='')
        id.meta['tip'] = "the unique identifier of the experiment"
        
        ncount = pyre.inventory.str( 'ncount', default = 1e6 )
        ncount.meta['tip'] = 'number of neutrons'
        
        pass # end of Inventory


    def start(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page

        if self.inventory.id == '':
            #create a new experiment
            from vnf.dom.NeutronExperiment import NeutronExperiment
            experiment = director.clerk.new_ownedobject( NeutronExperiment )
            experiment.status = 'started'
            director.clerk.updateRecord( experiment )
            #need to reload the page so that id is correctly
            self.inventory.id = experiment.id
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
            pass
        
        main = page._body._content._main

        # populate the main column
        document = main.document(title='Neutron Experiment Wizard: start')
        document.description = ''
        document.byline = 'byline?'

        p = document.paragraph()
        p.text = [
            'To run a virtual neutron experiment, you will need to select',
            'a neutron instrument, prepare your sample, put your',
            'sample in a sample holder, select instrument parameters',
            'for this experiment, and finally pick a computation server',
            'to run your virtual neutron experiment.',
            'Default values are provided for all these characteristics',
            'of the experiment, but please review them before launching',
            'your simulation.',
            ]

        p = document.paragraph()
        p.text = [
            'Please first assign a name to this experiment:',
            ]

        formcomponent = self.retrieveFormToShow(
            'neutronexperimentwizard_start' )
        formcomponent.inventory.experiment_id = self.inventory.id
        formcomponent.director = director
        
        # create form
        form = document.form(
            name='start',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = '', routine = 'verify_experiment_name',
            id = self.inventory.id,
            arguments = {'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        # run button
        submit = form.control(name="actor.form-received.submit", type="submit", value="Continue")

#        self._footer( document, director )
        return page


    def verify_experiment_name(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page

        self.processFormInputs( director )

        experiment = director.clerk.getNeutronExperiment(
            self.inventory.id)
        if experiment.short_description in ['', None, 'None']:
            return self.start( director )

        if experiment.status == 'started':
            experiment.status = 'partially configured'
            director.clerk.updateRecord( experiment )
        return self.select_instrument( director )
    

    def select_instrument(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page

        experiment = director.clerk.getNeutronExperiment(
            self.inventory.id)

        main = page._body._content._main

        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: select neutron instrument')
        document.description = ''
        document.byline = 'byline?'

        formcomponent = self.retrieveFormToShow( 'selectneutroninstrument' )
        formcomponent.inventory.experiment_id = self.inventory.id
        formcomponent.director = director
        
        # create form
        form = document.form(
            name='selectneutroninstrument',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = '', routine = 'configure_instrument',
            id = self.inventory.id,
            arguments = {'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        # run button
        submit = form.control(name="submit", type="submit", value="Continue")
            
#        self._footer( document, director )
        return page


    def configure_instrument(self, director, errors = None):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page

        self.processFormInputs( director )

        id = self.inventory.id
        experiment = director.clerk.getNeutronExperiment( id )
        configured_instrument_id = experiment.instrument_id
        configured_instrument = director.clerk.getConfiguredInstrument(
            configured_instrument_id)
        instrument_id = configured_instrument.instrument_id

        main = page._body._content._main

        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: instrument configuration')
        document.description = ''
        document.byline = 'byline?'

        formname = 'configure_%s_instrument' % (
            instrument_id
            .lower().replace(' ','_').replace( '-', '_' ), )

        #raise RuntimeError, formname
        formcomponent = self.retrieveFormToShow(formname)
        if formcomponent is None:
            formcomponent = self.retrieveFormToShow('configureneutroninstrument')
            pass # end if

        formcomponent.inventory.id = configured_instrument_id
        formcomponent.director = director
        
        # create form
        form = document.form(
            name='configureinstrument',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = '', routine = 'verify_instrument_configuration',
            id = self.inventory.id,
            arguments = {'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form, errors = errors )
        
        # run button
        submit = form.control(name="submit", type="submit", value="Continue")
        
#        self._footer( document, director )
        return page
    
    
    def verify_instrument_configuration(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
        
        try:
            self.processFormInputs( director )
        except InputProcessingError, err:
            errors = err.errors
            self.form_received = None
            director.routine = 'configure_instrument'
            return self.configure_instrument( director, errors = errors )

        experiment = director.clerk.getNeutronExperiment(
            self.inventory.id )
        # make sure instrument is configured
        if empty_id( experiment.instrument_id ):
            director.routine = 'select_instrument'
            return self.select_instrument( director )
        # get configured instrument
        configured_instrument = director.clerk.getConfiguredInstrument(
            experiment.instrument_id )
        # make sure it has a instrument and it is configured
        if empty_id( configured_instrument.instrument_id ) or \
           empty_id( configured_instrument.configuration_id ):
            director.routine = 'select_instrument'
            return self.select_instrument( director )

        # update experiment status
        director.clerk.updateRecord( experiment )
        
        director.routine = 'sample_environment'
        return self.sample_environment(director)
        

    def sample_environment(self, director, errors = None):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
                
        #get experiment
        experiment_id = self.inventory.id
        experiment = director.clerk.getNeutronExperiment( experiment_id )

        main = page._body._content._main

        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: sample environment')
        document.description = ''
        document.byline = 'byline?'

        #sample environment
        sampleenvironment_id = experiment.sampleenvironment_id

        formcomponent = self.retrieveFormToShow( 'sample_environment' )
        formcomponent.inventory.id = sampleenvironment_id
        formcomponent.director = director
        
        # create form
        form = document.form(
            name='sample environment',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = '',
            routine = 'verify_sample_environment',
            id = self.inventory.id,
            arguments = {'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form, errors = errors )
        
        # run button
        submit = form.control(name="submit", type="submit", value="Continue")
        
#        self._footer( document, director )
        return page


    def verify_sample_environment(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
        
        try:
            sampleenvironment = self.processFormInputs( director )
        except InputProcessingError, err:
            errors = err.errors
            self.form_received = None
            director.routine = 'sample_environment'
            return self.sample_environment( director, errors = errors )

        experiment = director.clerk.getNeutronExperiment(
            self.inventory.id)
        if empty_id( experiment.sampleenvironment_id ):
            experiment.sampleenvironment_id = sampleenvironment.id
            director.clerk.updateRecord( experiment )
        else:
            assert experiment.sampleenvironment_id == sampleenvironment.id
        director.clerk.updateRecord( experiment )

        director.routine = 'sample_preparation'
        return self.sample_preparation( director )
            

    def sample_preparation(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page

        experiment = director.clerk.getNeutronExperiment(
            self.inventory.id)

        main = page._body._content._main
        
        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: sample preparation')
        document.description = ''
        document.byline = 'byline?'
        
        formcomponent = self.retrieveFormToShow( 'sample_preparation' )
        formcomponent.inventory.experiment_id = self.inventory.id
        formcomponent.director = director
        
        # create form
        form = document.form(
            name='sample preparation',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = '',
            routine = 'configure_sample',
            id = self.inventory.id,
            arguments = {'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        # run button
        submit = form.control(name="submit", type="submit", value="Continue")
        
#        self._footer( document, director )
        return page

    

    def select_sample_from_sample_library(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
#        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        main = page._body._content._main
        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: Select a sample')
        document.description = ''
        document.byline = '<a href="http://danse.us">DANSE</a>'        
        
        formcomponent = self.retrieveFormToShow( 'sampleLibrary')
        formcomponent.director = director
        # build the form 
        form = document.form(name='', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'neutronexperimentwizard', 
            sentry = director.sentry,
            routine = 'configure_scatteringkernels',
            label = '',
            id=self.inventory.id,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        
                
        p = form.paragraph()
        p.text = [action_link(
        actionRequireAuthentication(
        'neutronexperimentwizard', director.sentry,
        label = 'Add a new sample',
        #routine = 'create_new_sample',
        routine = 'input_material',
        id=self.inventory.id
        ),  director.cgihome),'<br>']
        
        submit = form.control(name='submit',type="submit", value="next")
        #self.processFormInputs(director)
#        self._footer( form, director )
        return page           
     

    def input_material(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
#        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        main = page._body._content._main
        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: Create a new sample')
        document.description = ''
        document.byline = '<a href="http://danse.us">DANSE</a>'        
        
        formcomponent = self.retrieveFormToShow( 'input_material')
        formcomponent.director = director
        # build the form 
        form = document.form(name='', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'neutronexperimentwizard', 
            sentry = director.sentry,
            routine = 'configure_scatteringkernels',
            label = '',
            id=self.inventory.id,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        submit = form.control(name='submit',type="submit", value="next")
        #self.processFormInputs(director)
        self._footer( form, director )
        return page   


    def configure_sample(self, director, errors = None):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page        
        main = page._body._content._main
        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: sample configuration')
        document.description = ''
        document.byline = 'byline?'

        self.processFormInputs( director )

        #get experiment
        experiment = director.clerk.getNeutronExperiment(
            self.inventory.id )
        #get sample assembly
        sampleassembly = director.clerk.getSampleAssembly(
            experiment.sampleassembly_id )
        #get sample
        configured_scatterers = director.clerk.getConfiguredScatterers(
            experiment.sampleassembly_id )
        samples = filter(
            lambda configured: configured.label == 'sample',
            configured_scatterers )
        assert len(samples)==1, 'there should be only 1 sample in sample assembly %r' % sampleassembly.short_description
        sample = samples[0]

        #get descendennts
        sample = director.clerk.getHierarchy( sample )
        assert sample.scatterer is not None

        #In this step we obtain configuration of sample
        formname = 'configure%s%s' % (
            sample.scatterer.matter.realmatter.__class__.__name__.lower(),
            sample.scatterer.shape.realshape.__class__.__name__.lower(),
            )
        formcomponent = self.retrieveFormToShow(formname)
        formcomponent.inventory.id = sample.id
        formcomponent.director = director
        
        # create form
        form = document.form(
            name='configure sample',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = '',
            routine = 'verify_sample_configuration',
            id = self.inventory.id,
            arguments = {'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form, errors = errors )

        # run button
        submit = form.control(name="submit", type="submit", value="Continue")
        
#        self._footer( document, director )
        return page


    def verify_sample_configuration(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page

        try:
            self.processFormInputs(director)
        except InputProcessingError, err:
            errors = err.errors
            self.form_received = None
            director.routine = 'configure_sample'
            return self.configure_sample( director, errors = errors )            

        experiment = director.clerk.getNeutronExperiment(
            self.inventory.id )
        sampleassembly_id = experiment.sampleassembly_id
        if empty_id( sampleassembly_id ):
            raise RuntimeError, "sample assembly not set up"

        sampleassembly = director.clerk.getSampleAssembly( sampleassembly_id )
        scatterers = director.clerk.getConfiguredScatterers(sampleassembly_id)
        samples = filter(
            lambda scatterer: scatterer.label == 'sample',
            scatterers)
        if len(samples) != 1:
            raise RuntimeError, 'there should be one sample in the sample assembly'
        sample = samples[0]
        
        configured_sample = sample

        prototype_id = configured_sample.scatterer_id
        if empty_id(prototype_id):
            raise RuntimeError, "sample prototype not established"
        
        sample_prototype = director.clerk.getScatterer(prototype_id)
        
        director.clerk.updateRecord( experiment )

        return self.configure_scatteringkernels(director)


    def configure_scatteringkernels(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
#        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        main = page._body._content._main
        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: Scattering kernel selection')
        document.description = ''
        document.byline = '<a href="http://danse.us">DANSE</a>'        
        
        formcomponent = self.retrieveFormToShow( 'scatteringkernel')
        formcomponent.director = director
        # build the form 
        form = document.form(name='', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'neutronexperimentwizard', 
            sentry = director.sentry,
            routine = 'submit_experiment',
            label = '',
            id=self.inventory.id,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        
        p = form.paragraph()
        p.text = [action_link(
        actionRequireAuthentication(
        'neutronexperimentwizard', 
        director.sentry,
        label = 'Add a new scattering kernel',  
        routine='selectkernel',
        id=self.inventory.id),
        director.cgihome
        ),
        '<br>']
        
        submit = form.control(name='submit',type="submit", value="next")
        
        #self.processFormInputs(director)
        self._footer( form, director )
        return page  


    def selectkernel(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
#        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        main = page._body._content._main
        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: Kernel origin selection')
        document.description = ''
        document.byline = '<a href="http://danse.us">DANSE</a>'        
        
        formcomponent = self.retrieveFormToShow( 'selectkernel')
        formcomponent.director = director
        # build the form 
        form = document.form(name='', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'neutronexperimentwizard', 
            sentry = director.sentry,
            routine = 'onSelect',
            id=self.inventory.id,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        submit = form.control(name='submit',type="submit", value="next")
        #self.processFormInputs(director)
        self._footer( form, director )
        return page    
    
    def onSelect(self, director):
        selected = self.processFormInputs(director)
        method = getattr(self, selected )
        return method( director )

    def gulp(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main
        document = main.document(title='Classical atomistics kernel' )
        document.byline = '<a href="http://danse.us">DANSE</a>'    
        
        formcomponent = self.retrieveFormToShow( 'gulp')
        formcomponent.director = director
        # build the form form
        form = document.form(name='', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'neutronexperimentwizard', 
            sentry = director.sentry,
            routine = 'kernel_generator',
            id=self.inventory.id,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        next = form.control(name='submit',type="submit", value="next")
#        self._footer( document, director )
        return page 
   
    def localOrbitalHarmonic(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main
        document = main.document(title='Local orbital DFT energies, harmonic dynamics kernel' )
        document.byline = '<a href="http://danse.us">DANSE</a>'    
        
        formcomponent = self.retrieveFormToShow( 'abInitioHarmonic')
        formcomponent.director = director
        # build the form form
        form = document.form(name='', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'neutronexperimentwizard', 
            sentry = director.sentry,
            routine = 'kernel_generator',
            id=self.inventory.id,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        next = form.control(name='submit',type="submit", value="next")
#        self._footer( document, director )
        return page 
    
    def planeWaveHarmonic(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main
        document = main.document(title='Plane wave DFT energies, harmonic dynamics kernel' )
        document.byline = '<a href="http://danse.us">DANSE</a>'    
        
        formcomponent = self.retrieveFormToShow( 'abInitioHarmonic')
        formcomponent.director = director
        # build the form form
        form = document.form(name='', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'neutronexperimentwizard', 
            sentry = director.sentry,
            routine = 'kernel_generator',
            id=self.inventory.id,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        next = form.control(name='submit',type="submit", value="next")
#        self._footer( document, director )
        return page 
    
    def kernel_generator(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main
        document = main.document(title='Kernel Generator' )
        document.byline = '<a href="http://danse.us">DANSE</a>'        
        
        formcomponent = self.retrieveFormToShow( 'inelasticScatteringIntensity')
        formcomponent.director = director
        # build the form form
        form = document.form(name='', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'neutronexperimentwizard', 
            sentry = director.sentry,
            routine = 'submit_experiment',
            label = '',
            id = self.inventory.id,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        next = form.control(name='submit',type="submit", value="next")
#        self._footer( document, director )
        return page     


    def submit_experiment(self, director, errors = None):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page

        self._checkstatus( director )
        if not self.instrument_configured or not self.name_assigned or \
               not self.sample_environment_configured or \
               not self.sample_prepared or not self.kernel_configured:
            return self._showstatus( director )
        
        main = page._body._content._main
        # populate the main column
        document = main.document(title='Neutron Experiment Wizard: submit')
        document.description = ''
        document.byline = 'byline?'

        #In this step we obtain configuration of sample
        
        formcomponent = self.retrieveFormToShow( 'experiment_submission' )
        formcomponent.inventory.id = self.inventory.id
        formcomponent.director = director
        
        # create form
        form = document.form(
            name='experiment submission',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = '',
            routine = 'verify_experiment_submission',
            id = self.inventory.id,
            arguments = {'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form, errors = errors )

        # run button
        submit = form.control(name="actor.form-received.submit", type="submit", value="Submit")
        #back = form.control(name="actor.form-received.submit", type="submit", value="back")

#        self._footer( document, director )
        return page


    def verify_experiment_submission(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
        
        try:
            self.processFormInputs( director )
        except InputProcessingError, err:
            errors = err.errors
            self.form_received = None
            director.routine = 'submit_experiment'
            return self.submit_experiment( director, errors = errors )

        #get experiment
        experiment = director.clerk.getNeutronExperiment(
            self.inventory.id)
        #make sure experiment is configured all the way
        self._checkstatus(director)
        assert self.allconfigured == True
        
        #get full hierarchy
        experiment = director.clerk.getHierarchy( experiment )

        job = experiment.job
        from JobDataManager import JobDataManager
        path = JobDataManager( job, director ).localpath()

        username = director.sentry.username
        if username in ['demo']:
            #demo user can not really run simulation#
            #but they can see a demo
            from NeutronExperimentSimulationRunBuilder_demo import Builder
        else:
            from NeutronExperimentSimulationRunBuilder import Builder
        Builder(path).render(experiment)

        experiment.status = 'constructed'
        director.clerk.updateRecord( experiment )
        
        return self.showExperimentStatus(director)


    def showExperimentStatus(self,director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page        

        # just a redirection
        routine = director.routine = 'view'
        actor = director.retrieveActor( 'neutronexperiment')
        director.configureComponent( actor )
        actor.inventory.id = self.inventory.id
        director.actor = actor
        return getattr(actor, routine)( director )
    

    def verify_experiment_submission1(self, director):
        # just to show the back button
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page        

        if self.form_received.submit == 'back':
            return self.start(director)

        return page


    def save_experiment(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page        
        #nothing need to be done.
        #just go to the experiment list

        routine = director.routine = 'listall'
        actor = director.retrieveActor( 'neutronexperiment')
        director.configureComponent( actor )
        actor.inventory.id = self.inventory.id
        return getattr(actor, routine)( director )


    def cancel(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page        

        # remove this experiment
        experiment = director.clerk.getNeutronExperiment(
            self.inventory.id)
        director.clerk.deleteRecord( experiment )

        # go to greeter
        actor = director.retrieveActor( 'greet')
        director.configureComponent( actor )
        director.actor = actor
        return getattr(actor, 'default')( director )


    def __init__(self, name=None):
        if name is None:
            name = "neutronexperimentwizard"
        super(NeutronExperimentWizard, self).__init__(name)
        self.started \
                     = self.name_assigned \
                     = self.instrument_configured \
                     = self.sample_environment_configured \
                     = self.sample_prepared \
                     = self.kernel_configured \
                     = self.allconfigured \
                     = False
        return


    def _configure(self):
        base._configure(self)
        self.id = self.inventory.id
        return


    def _footer(self, document, director):
        #
        document.paragraph()

        p = document.paragraph(align = 'right')
        action = actionRequireAuthentication(
            label = 'Cancel',
            actor = 'neutronexperimentwizard',
            routine = 'cancel',
            id = self.inventory.id,
            sentry = director.sentry)
        link = action_link( action, director.cgihome )
        p.text = [
            '%s this experiment planning.' % link,
            ]
        return

    
    def _showstatus(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        # populate the main column
        document = main.document(title='Neutron Experiment Wizard: status')
        document.description = ''
        document.byline = 'byline?'

        p = document.paragraph()
        p.text = [
            'You experiment is not yet ready for submission.',
            'Please',
            ]

        d = {
            'name_assigned':  ('assign a name to this experiment',
                               'start'),
            'instrument_configured': ('select and configure an instrument',
                                      'select_instrument'),
            'sample_environment_configured': ('configure sample environment',
                                              'sample_environment'),
            'sample_prepared': ('prepare a sample',
                                'sample_preparation'),
            'kernel_configured': ('configure scattering kernel for sample',
                                  'kernel_origin'),
            }
        items = [ 'name_assigned', 'instrument_configured',
                  'sample_environment_configured',
                  'sample_prepared', 'kernel_configured',
                  ]
        for item in items:
            label, routine = d[item]
            if not getattr(self, item):
                action = actionRequireAuthentication(
                    actor = 'neutronexperimentwizard',
                    sentry = director.sentry,
                    label = label,
                    routine = routine,
                    id = self.inventory.id,
                    )
                link = action_link( action, director.cgihome)
                p.text.append( '%s,' % link )
                pass # endif
            continue

##        self._footer( document, director )
        return page
        

    def _checkstatus(self, director):
        experiment = director.clerk.getNeutronExperiment(
            self.inventory.id )
        self.name_assigned = experiment.short_description not in [None, '']

        instrument_id = experiment.instrument_id
        if not empty_id( instrument_id ):
            configured = director.clerk.getConfiguredInstrument(instrument_id)
            self.instrument_configured = not empty_id( configured.instrument_id )
            pass

        sampleenvironment_id = experiment.sampleenvironment_id
        self.sample_environment_configured = not empty_id( sampleenvironment_id )
        
        sampleassembly_id = experiment.sampleassembly_id
        
        if not empty_id( sampleassembly_id ):
            sampleassembly = director.clerk.getSampleAssembly(
                sampleassembly_id )
            
            scatterers = director.clerk.getConfiguredScatterers(
                sampleassembly_id)
            samples = filter(
                lambda scatterer: scatterer.label == 'sample',
                scatterers)
            if len(samples) == 0: return
            if len(samples) > 1: raise RuntimeError, "more than 1 sample"
            
            sample = samples[0]
            self.sample_prepared = not empty_id(sample.scatterer_id)
            # need to test if kernel is configured
            # ...
            # probably need a canned solution here for the demo...
            self.kernel_configured = True
            pass

        if not self.kernel_configured: return

        if experiment.ncount <=0 : return
        if empty_id(experiment.job_id): return
        job = director.clerk.getJob( experiment.job_id )

        self.allconfigured = True

        # the last is to check if all files for this experiment
        # are generated
        return        


    pass # end of NeutronExperimentWizard



from misc import new_id, empty_id


# version
__id__ = "$Id$"

# End of file 
