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
            #change status to "started"
            director.db.updateRow( NeutronExperiment, [ ('status','started') ] )
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
            label = '', routine = 'verify_instrument_selection',
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


    def verify_instrument_selection(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
        
        try:
            self.processFormInputs( director )
        except InputProcessingError, err:
            errors = err.errors
            self.form_received = None
            director.routine = 'select_instrument'
            return self.select_instrument( director, errors = errors )

        experiment = director.clerk.getNeutronExperiment(
            self.inventory.id )
        instrument = experiment.instrument.dereference(director.db)

        configuration_ref = experiment.instrument_configuration
        if configuration_ref is not None:
            configuration = configuration_ref.dereference(director.db)
            configuration_target = configuration.target
            if configuration_target != instrument.id:
                # the current configuration is not for the selected instrument
                # remove the current configuration
                director.clerk.deleteRecord( configuration )

                # update experiment record
                experiment.instrument_configuration = None
                director.clerk.updateRecord( experiment )
        
        director.routine = 'configure_instrument'
        return self.configure_instrument(director)


    def configure_instrument(self, director, errors = None):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page

        self.processFormInputs( director )

        id = self.inventory.id
        experiment = director.clerk.getNeutronExperiment( id )

        main = page._body._content._main

        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: instrument configuration')
        document.description = ''
        document.byline = 'byline?'

        formname = 'configure_%s_instrument' % (
            experiment.instrument.id
            .lower().replace(' ','_').replace( '-', '_' ), )

        formcomponent = self.retrieveFormToShow(formname)
        if formcomponent is None:
            formcomponent = self.retrieveFormToShow('configureneutroninstrument')
            pass # end if

        configuration = experiment.instrument_configuration
        if configuration is None:
            formcomponent.inventory.id = None
        else:
            formcomponent.inventory.id = configuration.id
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
            configuration = self.processFormInputs( director )
        except InputProcessingError, err:
            errors = err.errors
            self.form_received = None
            director.routine = 'configure_instrument'
            return self.configure_instrument( director, errors = errors )

        experiment = director.clerk.getNeutronExperiment(
            self.inventory.id )
        old_configuration = experiment.instrument_configuration
        if old_configuration is not None:
            # clear the old configuration
            old_configuration = old_configuration.dereference( director.db )
            director.clerk.deleteRecord( old_configuration )
        experiment.instrument_configuration = configuration
        
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

        formcomponent = self.retrieveFormToShow( 'sample_environment' )
        
        sampleenvironment = experiment.sampleenvironment
        if sampleenvironment is None:
            formcomponent.inventory.id = None
        else:
            formcomponent.inventory.id = sampleenvironment.id
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

        assert sampleenvironment is not None
        
        experiment = director.clerk.getNeutronExperiment(
            self.inventory.id)
        environ = experiment.sampleenvironment
        # if originally the experiment has not been assigned a sample environment
        # make assignment now
        if environ is None:
            experiment.sampleenvironment = sampleenvironment
            director.clerk.updateRecord( experiment )

        director.routine = 'sample_preparation'
        return self.sample_preparation( director )


    def sample_preparation(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page

        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        sample = _get_sample_from_experiment(experiment)
        if sample is None:
            return self.fresh_sample_preparation(director)
        
        main = page._body._content._main
        
        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: sample preparation')
        document.description = ''
        document.byline = 'byline?'

        p = document.paragraph()
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = 'configure',
            routine = 'configure_sample',
            id = self.inventory.id,
            )
        link = action_link( action, director.cgihome )
        p.text = [
            'You have already created your sample.',
            'You may want to %s this sample.' % link,
            ]

        p = document.paragraph()
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = 'select',
            routine = 'select_sample_from_examples',
            id = self.inventory.id,
            )
        link = action_link( action, director.cgihome )
        p.text = [
             'The easisest way to start would be to',
             '%s from a bunch of basic samples.' % link,
            ]

        #p = document.paragraph()
        #action = actionRequireAuthentication(
        #    actor = 'neutronexperimentwizard', sentry = director.sentry,
        #    label = 'select a sample from your own sample library',
        #    routine = 'select_sample_from_sample_library',
        #    id = self.inventory.id,
        #    )
        #link = action_link( action, director.cgihome )
        #p.text = [
        #    'Or you could %s.' % link,
        #    ]

        p = document.paragraph()
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = 'create a new sample from scratch',
            routine = 'create_new_sample',
            id = self.inventory.id,
            )
        link = action_link( action, director.cgihome )
        p.text = [
            'Also you could %s.' % link,
            ]

        return page


    def fresh_sample_preparation(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page

        main = page._body._content._main
        
        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: sample preparation')
        document.description = ''
        document.byline = 'byline?'
        
        p = document.paragraph()
        p.text = [
            'Sample is the heart of your experiment. By placing',
            'your sample in the neutron beam of a neutron instrument,',
            'you can study, for example, phonons or mangons',
            'in your sample.',
            ]

        p = document.paragraph()
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = 'select',
            routine = 'select_sample_from_examples',
            id = self.inventory.id,
            )
        link = action_link( action, director.cgihome )
        p.text = [
             'The easisest way to start would be to',
             '%s from a bunch of basic samples.' % link,
            ]

        #p = document.paragraph()
        #action = actionRequireAuthentication(
        #    actor = 'neutronexperimentwizard', sentry = director.sentry,
        #    label = 'select a sample from your own sample library',
        #    routine = 'select_sample_from_sample_library',
        #    id = self.inventory.id,
        #    )
        #link = action_link( action, director.cgihome )
        #p.text = [
        #    'Or you could %s.' % link,
        #    ]

        p = document.paragraph()
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = 'create a new sample from scratch',
            routine = 'create_new_sample',
            id = self.inventory.id,
            )
        link = action_link( action, director.cgihome )
        p.text = [
            'Also you could %s.' % link,
            ]

        return page
            

    def select_sample_from_examples(self, director):
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
        
        formcomponent = self.retrieveFormToShow( 'select_sample_from_examples' )
        formcomponent.inventory.experiment_id = self.inventory.id
        formcomponent.director = director
        
        # create form
        form = document.form(
            name='select sample',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = '',
            routine = 'verify_sample_selection',
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


    def verify_sample_selection(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperimentwizard' )
        except AuthenticationError, err:
            return err.page
        
        scatterer_id = self.processFormInputs( director )

        experiment = director.clerk.getNeutronExperiment(
            self.inventory.id )

        oldsample = _get_sample_from_experiment(experiment)
        if oldsample:
            # if so, remove the reference from the referenceset
            scatterers_refset.delete( oldsample, director.db )

        # the user chosen scatterer
        sample = director.clerk.getScatterer( scatterer_id )
        
        #now make a copy
        samplecopy = director.clerk.deepcopy( sample )

        #and add to the sample assembly
        scatterers_refset.add( samplecopy, director.db, name = 'sample' )

        #redirect
        director.routine = 'configure_sample'
        return self.configure_sample(director)

    

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

        #self.processFormInputs( director )

        #get experiment
        experiment = director.clerk.getNeutronExperiment(
            self.inventory.id )

        #sample
        sample = _get_sample_from_experiment(experiment)
        if sample is None: raise RuntimeError, "No sample in sample assembly"

        #In this step we obtain configuration of sample
        formname = 'configure%s%s' % (
            sample.matter.dereference(director.db).__class__.__name__.lower(),
            sample.shape.dereference(director.db).__class__.__name__.lower(),
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
        sampleassembly = experiment.sampleassembly.dereference( director.db )
        scatterers_refset = sampleassembly.scatterers
        scatterers = scatterers_refset.dereference(director.db)

        sample = None
        for name, s in scatterers:
            if name == 'sample': sample = s; break;
            continue

        if sample is None: raise RuntimeError, "No sample in sample assembly"
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
            title='Neutron Experiment Wizard: Scattering kernel configuration')
        document.description = ''
        document.byline = '<a href="http://danse.us">DANSE</a>'

        experiment = director.clerk.getNeutronExperiment( self.inventory.id )
        sampleassembly = experiment.sampleassembly.dereference(director.db)
        sample = _get_sample_from_sampleassembly( sampleassembly, director.db )
        kernels = _get_kernels_from_scatterer( sample, director.db )

        #hack
        name, kernel = kernels[0]

        kernelclass = kernel.__class__
        formcomponent = self.retrieveFormToShow( kernelclass.__name__.lower() )
        formcomponent.director = director
        formcomponent.inventory.id = kernel.id
        
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
        
        job = experiment.job.dereference(director.db)
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

        instrument_ref = experiment.instrument
        self.instrument_configured = not nullpointer( instrument_ref )

        sampleenvironment_ref = experiment.sampleenvironment
        self.sample_environment_configured = not nullpointer(sampleenvironment_ref)
        
        if self.sample_environment_configured:
            sampleassembly_ref = experiment.sampleassembly
            sampleassembly = sampleassembly_ref.dereference(director.db)
            sample = _get_sample_from_sampleassembly( sampleassembly, director.db )
            
            self.sample_prepared = not nullpointer(sample)
            # need to test if kernel is configured
            # ...
            # probably need a canned solution here for the demo...
            self.kernel_configured = True
            pass

        if not self.kernel_configured: return

        if experiment.ncount <=0 : return
        if nullpointer(experiment.job): return
        job = experiment.job.dereference(director.db)

        self.allconfigured = True

        # the last is to check if all files for this experiment
        # are generated
        return        


    pass # end of NeutronExperimentWizard


def _get_sample_from_experiment(experiment, db):
    sampleassembly_ref = experiment.sampleassembly
    sampleassembly = sampleassembly_ref.dereference(db)
    return _get_sample_from_sampleassembly(sampleassembly_ref)


def _get_sample_from_sampleassembly(sampleassembly, db):
    scatterers_refset = sampleassembly.scatterers
    scatterers = scatterers_refset.dereference(db)
    sample = None
    for name, s in scatterers:
        if name == 'sample': sample = s; break
        continue
    return sample


def _get_kernels_from_scatterer(scatterer, db):
    kernels_refset = scatterer.kernels
    kernels = kernels_refset.dereference(db)
    return kernels


from misc import new_id, empty_id, nullpointer

# version
__id__ = "$Id$"

# End of file 
