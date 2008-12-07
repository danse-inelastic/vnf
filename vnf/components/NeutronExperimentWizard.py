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

        kernel_id = pyre.inventory.str('kernel_id', default='')
        kernel_type = pyre.inventory.str('kernel_type', default='')
        
        ncount = pyre.inventory.str( 'ncount', default = 1e6 )
        ncount.meta['tip'] = 'number of neutrons'

        # the element to edit. a tuple of tablename, id
        editee = pyre.inventory.str('editee', default='')
        
        pass # end of Inventory


    def start(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        if self.inventory.id == '':
            # create a new experiment
            from vnf.dom.NeutronExperiment import NeutronExperiment
            experiment = director.clerk.newOwnedObject( NeutronExperiment )
            # *** the following line is for Brandon ***
            #   experiment.instrument = 'TestInstrument'
            # change status to "started"
            experiment.status = 'started'
            director.clerk.updateRecord(experiment)
            # need to reload the page so that id is correctly
            self.inventory.id = experiment.id
            page = self._retrievePage(director)
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
            page = self._retrievePage(director)
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
            page = self._retrievePage(director)
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
        instrument = experiment.instrument
        if instrument: instrument_id = instrument.id
        else: instrument_id = None
        formcomponent.expand( form, instrument_id = instrument_id )

        # run button
        submit = form.control(name="submit", type="submit", value="Continue")
            
#        self._footer( document, director )
        return page


    def verify_instrument_selection(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page
        
        try:
            instrument_id = self.processFormInputs( director )
        except InputProcessingError, err:
            errors = err.errors
            self.form_received = None
            director.routine = 'select_instrument'
            return self.select_instrument( director, errors = errors )

        experiment = director.clerk.getNeutronExperiment(
            self.inventory.id )
        experiment.instrument = instrument_id
        director.clerk.updateRecord(experiment)

        # the instruemnt
        instrument = director.clerk.dereference(experiment.instrument)
        
        # make sure instrument configuration is good
        configuration_ref = experiment.instrument_configuration
        if configuration_ref:
            # if there is an old configuration, make sure
            # that configuration is for the same instrument
            configuration = director.clerk.dereference(configuration_ref)
            configuration_target = configuration.target
            if configuration_target.id != instrument.id:
                # the current configuration is not for the selected instrument
                # remove the current configuration
                director.clerk.deleteRecord(configuration)
                
                # update experiment record
                experiment.instrument_configuration = None
                director.clerk.updateRecord(experiment)
                configuration_ref = None

        # if there is no configuration, create one
        if not configuration_ref:
            configuration = director.clerk.newInstrumentConfiguration(instrument)
            experiment.instrument_configuration = configuration
            director.clerk.updateRecord(experiment)

        director.routine = 'configure_instrument'
        return self.configure_instrument(director)


    def configure_instrument(self, director, errors = None):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

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
            return self.configure_neutron_components(director)

        configuration = experiment.instrument_configuration
        if configuration is None:
            raise RuntimeError, "instrument configuration not initd: experiment %s" % id
        else:
            formcomponent.inventory.type = configuration.table
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
            page = self._retrievePage(director)
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
            old_configuration = director.clerk.dereference(old_configuration)
            director.clerk.deleteRecord( old_configuration )
        experiment.instrument_configuration = configuration
        
        # update experiment status
        director.clerk.updateRecord( experiment )

        instrument = director.clerk.dereference(experiment.instrument)
        if _instrument_without_sample(instrument, director.clerk.db):
            routine = 'submit_experiment'
        else: routine = 'sample_environment'
        director.routine = routine
        return getattr(self, routine)(director)


    def configure_neutron_components(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        id = self.inventory.id
        if not id: raise RuntimeError, "id not specified"

        # get neutron components
        experiment = director.clerk.getNeutronExperiment(id)
        instrument = director.clerk.dereference(experiment.instrument)
        instrument_configuration = director.clerk.dereference(
            experiment.instrument_configuration)
        components = director.clerk.dereference(instrument_configuration.components)

        main = page._body._content._main
        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: configuration of instrument %s' % instrument.short_description)
        document.description = ''
        document.byline = 'byline?'

        # create a dummy form
        form = document.form(
            name='configure instrument components',
            legend= 'Components of instrument',
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = '',
            routine = 'verify_neutron_components_configuration',
            id = self.inventory.id,
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # present the component list
        for name, component in components:
            p = form.paragraph()
            action = actionRequireAuthentication(
                actor = 'neutronexperimentwizard', sentry = director.sentry,
                label = 'edit',
                routine = 'edit_neutron_component',
                id = self.inventory.id,
                editee = '%s,%s' % (component.name, component.id)
                )
            editlink = action_link( action, director.cgihome )
            p.text = [
                '%s: (%s)' % (
                name,
                editlink,
                )
                ]
            continue
        
        # run button
        submit = form.control(name="submit", type="submit", value="Continue")
        return page


    def verify_neutron_components_configuration(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page
        
        #
        id = self.inventory.id
        if not id: raise RuntimeError
        experiment = director.clerk.getNeutronExperiment(id)
        ic_ref = experiment.instrument_configuration
        if not ic_ref: raise RuntimeError

        ic = director.clerk.dereference(ic_ref)
        ic.configured = True
        director.clerk.updateRecord(ic)
        
        # specify action
        instrument = director.clerk.dereference(experiment.instrument)
        if _instrument_without_sample(instrument, director.clerk.db):
            routine = 'submit_experiment'
        else: routine = 'sample_environment'
        return getattr(self, routine)(director)
    

    def edit_neutron_component(self, director, errors=None):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        editee = self.inventory.editee
        tablename, id = editee.split(',')
        component = director.clerk.getRecordByID(tablename, id)
        typename = component.__class__.__name__

        main = page._body._content._main
        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: %s %s' % (
            typename, component.id))
        document.description = ''
        document.byline = 'byline?'

        formcomponent = self.retrieveFormToShow(typename.lower())
        formcomponent.inventory.id = component.id
        formcomponent.director = director
        
        # create form
        form = document.form(
            name=typename,
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = '', routine = 'verify_neutron_component_configuration',
            id = self.inventory.id,
            editee = editee,
            arguments = {'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand(form, errors=errors)

        # run button
        submit = form.control(name="actor.form-received.submit", type="submit", value="Continue")
        return page


    def verify_neutron_component_configuration(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page
        
        try:
            self.processFormInputs( director )
        except InputProcessingError, err:
            errors = err.errors
            self.form_received = None
            director.routine = 'edit_neutron_component'
            return self.edit_neutron_component( director, errors = errors )

        return self.configure_neutron_components(director)
        

    def sample_environment(self, director, errors = None):
        try:
            page = self._retrievePage(director)
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
            page = self._retrievePage(director)
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
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        sample = _get_sample_from_experiment(experiment, director.clerk.db)
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
            label = 'remove this sample and restart sample preparation',
            routine = 'restart_sample_preparation',
            id = self.inventory.id,
            )
        link = action_link( action, director.cgihome )
        p.text = [
            'Or you may want to %s?' % link
            ]

        return page


    def restart_sample_preparation(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        sampleassembly = _get_sampleassembly_from_experiment(experiment, director.clerk.db)
        if not sampleassembly: raise RuntimeError
        sample = _get_sample_from_sampleassembly(sampleassembly, director.clerk.db)
        if not sample: raise RuntimeError
        sampleassembly.scatterers.delete(sample, director.clerk.db)
        
        return self.fresh_sample_preparation(director)
        


    def fresh_sample_preparation(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        # if no sample assembly, add one
        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        sampleassembly = _get_sampleassembly_from_experiment(experiment, director.clerk.db)
        if not sampleassembly:
            from vnf.dom.SampleAssembly import SampleAssembly
            sampleassembly = director.clerk.newOwnedObject(SampleAssembly)
            experiment.sampleassembly = sampleassembly
            director.clerk.updateRecord(experiment)

        #
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
            page = self._retrievePage(director)
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
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page
        
        scatterer_id = self.processFormInputs( director )

        experiment = director.clerk.getNeutronExperiment(
            self.inventory.id )

        sampleassembly = _get_sampleassembly_from_experiment(experiment, director.clerk.db)
        scatterers_refset = sampleassembly.scatterers

        # check if there is an old sample
        oldsample = _get_sample_from_sampleassembly(sampleassembly, director.clerk.db)
        if oldsample:
            # if so, remove the reference from the referenceset
            sampleassembly = _get_sampleassembly_from_experiment(experiment, director.clerk.db)
            scatterers_refset.delete( oldsample, director.clerk.db )

        # the user chosen scatterer
        sample = director.clerk.getScatterer( scatterer_id )
        
        #now make a copy
        samplecopy = director.clerk.deepcopy( sample )

        #and add to the sample assembly
        scatterers_refset.add( samplecopy, director.clerk.db, name = 'sample' )

        #redirect
        director.routine = 'configure_sample'
        return self.configure_sample(director)

    

    def select_sample_from_sample_library(self, director):
        try:
            page = self._retrievePage(director)
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
            page = self._retrievePage(director)
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
            page = self._retrievePage(director)
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
        sample = _get_sample_from_experiment(experiment, director.clerk.db)
        if sample is None: raise RuntimeError, "No sample in sample assembly"

        #In this step we obtain configuration of sample
        formname = 'configure%s%s' % (
            director.clerk.dereference(sample.matter).__class__.__name__.lower(),
            director.clerk.dereference(sample.shape).__class__.__name__.lower(),
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
            page = self._retrievePage(director)
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
        sampleassembly = director.clerk.dereference(experiment.sampleassembly)
        scatterers_refset = sampleassembly.scatterers
        scatterers = director.clerk.dereference(scatterers_refset)

        sample = None
        for name, s in scatterers:
            if name == 'sample': sample = s; break;
            continue

        if sample is None: raise RuntimeError, "No sample in sample assembly"
        return self.material_simulation(director)


    def material_simulation(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        main = page._body._content._main
        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: material simulation and modeling')
        document.description = ''
        document.byline = 'byline?'

        p = document.paragraph()
        p.text = [
            'The purpose of material simulation or modeling is to obtain',
            'a systematic understanding of material properties (which)',
            'sometimes including scattering properties.',
            ]

        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        sample = _get_sample_from_experiment(experiment, director.clerk.db)
        
        simresults = director.clerk.findSimResults(sample)

        p = document.paragraph()
        if len(simresults):
            p.text = [
                'The following is a list of simulation or modeling results',
                'for your sample:',
                ]
            for r in simresults:
                p1 = document.paragraph()
                p1.text = [
                    '%s' % r,
                    ]
        else:
            p.text = [
                'No simulation has been done for your sample yet.'
                ]
            action = actionRequireAuthentication(        
                actor = 'materialsimulationwizard', 
                sentry = director.sentry,
                routine = 'start',
                label = 'the material simulation/modeling wizard',
                matterid = sample.matter.id,
                mattertype = sample.matter.table.__name__,
                )
            link = action_link( action, director.cgihome )
            p.text = [
                'You can use %s to perform your material simulation and then' % link,
                'come back here',
                ]
        return page


    def configure_scatteringkernels(self, director):
        experiment = director.clerk.getNeutronExperiment( self.inventory.id )
        sampleassembly = director.clerk.dereference(experiment.sampleassembly)
        sample = _get_sample_from_sampleassembly( sampleassembly, director.clerk.db )
        kernels = _get_kernels_from_scatterer( sample, director.clerk.db )

        if len(kernels):
            return self.present_kernels(director)

        return self.nokernelsyet(director)


    def nokernelsyet(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page
#        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        main = page._body._content._main
        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: No kernel')
        document.description = ''
        document.byline = '<a href="http://danse.us">DANSE</a>'

        p = document.paragraph()
        p.text = [
            'Scattering kernels describe scattering properties of a neutron scatterer.',
            ]
        
        p = document.paragraph()
        action = actionRequireAuthentication(          
            actor = 'neutronexperimentwizard', 
            sentry = director.sentry,
            routine = 'add_new_kernel_from_scratch',
            label = 'create',
            id = self.inventory.id,
            )
        link = action_link( action, director.cgihome )
        p.text = [
            'No scattering kernel has been defined.',
            'Please %s a new kernel' % link,
            ]
        return page


    def present_kernels(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page
#        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        main = page._body._content._main
        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: kernels')
        document.description = ''
        document.byline = '<a href="http://danse.us">DANSE</a>'

        p = document.paragraph()
        p.text = [
            'Scattering kernels describe scattering properties of a neutron scatterer.',
            'Following is a list of existing scattering kernels:',
            ]

        experiment = director.clerk.getNeutronExperiment( self.inventory.id )
        sampleassembly = director.clerk.dereference(experiment.sampleassembly)
        sample = _get_sample_from_sampleassembly( sampleassembly, director.clerk.db )
        kernels = _get_kernels_from_scatterer( sample, director.clerk.db )

        for label,kernel in kernels:
            p = document.paragraph()
            action = actionRequireAuthentication(          
                actor = 'neutronexperimentwizard', 
                sentry = director.sentry,
                routine = 'edit_kernel',
                label = 'edit',
                id = self.inventory.id,
                kernel_id = kernel.id,
                kernel_type = kernel.__class__.__name__,
                )
            edit_link = action_link( action, director.cgihome )

            action = actionRequireAuthentication(          
                actor = 'neutronexperimentwizard', 
                sentry = director.sentry,
                routine = 'delete_kernel',
                label = 'delete',
                id = self.inventory.id,
                kernel_id = kernel.id,
                kernel_type = kernel.__class__.__name__,
                )
            delete_link = action_link( action, director.cgihome )
            p.text = [
                'Kernel %s: (%s), (%s)' % (
                _describe_kernel(kernel), edit_link, delete_link,
                ),
                ]
            continue

        p = document.paragraph()
        action = actionRequireAuthentication(          
            actor = 'neutronexperimentwizard', 
            sentry = director.sentry,
            routine = 'add_new_kernel_from_scratch',
            label = 'add',
            id = self.inventory.id,
            )
        link = action_link( action, director.cgihome )
        p.text = [
            'You can also %s a new kernel.' % link,
            ]

        p = document.paragraph()
        action = actionRequireAuthentication(          
            actor = 'neutronexperimentwizard', 
            sentry = director.sentry,
            routine = 'submit_experiment',
            label = 'submit',
            id = self.inventory.id,
            )
        link = action_link( action, director.cgihome )
        p.text = [
            'If you are done with kernel configurations, you can %s your experiment.'
            % link,
            ]
        return page
    

    def edit_kernel(self, director, errors = None):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        main = page._body._content._main
        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: Scattering kernel configuration')
        document.description = ''
        document.byline = '<a href="http://danse.us">DANSE</a>'

        experiment = director.clerk.getNeutronExperiment( self.inventory.id )
        sample = _get_sample_from_experiment( experiment, director.clerk.db )
        if not sample: raise RuntimeError
        kernels = _get_kernels_from_scatterer( sample, director.clerk.db )

        kernel = None
        for label, k in kernels:
            if k.id == self.inventory.kernel_id: kernel = k; break
            continue

        if not kernel: raise RuntimeError

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
            routine = 'verify_kernel_configuration',
            label = '',
            id=self.inventory.id,
            kernel_id = self.inventory.kernel_id,
            kernel_type = self.inventory.kernel_type,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form, errors = errors )
        
        submit = form.control(name='submit',type="submit", value="next")
        
        #self.processFormInputs(director)
        #self._footer( form, director )
        return page


    def verify_kernel_configuration(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page
        
        try:
            self.processFormInputs( director )
        except InputProcessingError, err:
            errors = err.errors
            self.form_received = None
            director.routine = 'edit_kernel'
            return self.edit_kernel( director, errors = errors )
        
        return self.configure_scatteringkernels(director)


    def delete_kernel(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        sample = _get_sample_from_experiment(experiment, director.clerk.db)
        if not sample: raise RuntimeError

        kernels_refset = sample.kernels

        table, id = self.inventory.kernel_type, self.inventory.kernel_id
        kernel = director.clerk.getRecordByID(table,id)
        kernels_refset.delete( kernel, director.clerk.db )
        return self.configure_scatteringkernels(director)


    def new_kernel(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        #
        main = page._body._content._main
        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: new kernel')
        document.description = ''
        document.byline = 'byline?'
        
        p = document.paragraph()
        p.text = [
            'Scattering kernel describes the physics of neutron scattering',
            'of a neutron scatterer.',
            ]

        p = document.paragraph()
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = 'select',
            routine = 'add_kernel_from_examples',
            id = self.inventory.id,
            )
        link = action_link( action, director.cgihome )
        p.text = [
             'The easisest way to start would be to',
             '%s from a bunch of basic samples.' % link,
            ]

        p = document.paragraph()
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = 'create a new kernel from scratch',
            routine = 'add_new_kernel_from_scratch',
            id = self.inventory.id,
            )
        link = action_link( action, director.cgihome )
        p.text = [
            'Also you could %s.' % link,
            ] 
        return page


    def add_new_kernel_from_scratch(self, director):
        return self.select_kernel_type(director)
        return self.select_material_simulation_result(director)


    def select_material_simulation_result(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        sample = _get_sample_from_experiment(experiment)
        material = sample.matter
        
        #
        main = page._body._content._main
        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: add new kernel')
        document.description = ''
        document.byline = 'byline?'

        formcomponent = self.retrieveFormToShow( 'selectmaterialsimulationresult' )
        formcomponent.director = director
        formcomponent.inventory.material_type = material.table.__name__
        formcomponent.inventory.material_id = material.id
        
        # create form
        form = document.form(
            name='selectmaterialsimulationresult',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = '', routine = 'verify_materialsimulationresult_selection',
            id = self.inventory.id,
            arguments = {'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        # run button
        submit = form.control(name="submit", type="submit", value="OK")
        
        return page
    

    def select_kernel_type(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        #
        main = page._body._content._main
        # populate the main column
        document = main.document(
            title='Neutron Experiment Wizard: add new kernel')
        document.description = ''
        document.byline = 'byline?'

        formcomponent = self.retrieveFormToShow( 'selectkerneltype' )
        formcomponent.director = director
        
        # create form
        form = document.form(
            name='selectkerneltype',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = '', routine = 'verify_kerneltype_selection',
            id = self.inventory.id,
            arguments = {'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        # run button
        submit = form.control(name="submit", type="submit", value="OK")
        
        #self._footer( document, director )
        return page


    def verify_kerneltype_selection(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        typename = self.processFormInputs(director)
        exec 'from vnf.dom.%s import %s as table' % (typename, typename)
        kernel = director.clerk.newOwnedObject(table)

        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        sample = _get_sample_from_experiment(experiment, director.clerk.db)
        sample.kernels
        return page


    def selectkernel(self, director):
        try:
            page = self._retrievePage(director)
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
            page = self._retrievePage(director)
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
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main
        document = main.document(title='Local orbital DFT energies, harmonic dynamics kernel' )
        document.byline = '<a href="http://danse.us">DANSE</a>'    
        
        formcomponent = self.retrieveFormToShow( 'localOrbitalHarmonic')
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
            page = self._retrievePage(director)
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
            page = self._retrievePage(director)
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


    def submit_experiment(self, director, errors=None, id=None):
        if id is None: id = self.inventory.id
        else: self.inventory.id = id

        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        self._checkstatus( director )
        if not self.allconfigured:
##                (not self.instrument_configured or not self.name_assigned or \
##                 not self.sample_environment_configured or \
##                 not self.sample_prepared or not self.kernel_configured):
            return self._showstatus( director )

        main = page._body._content._main
        # populate the main column
        document = main.document(title='Neutron Experiment Wizard: submit')
        document.description = ''
        document.byline = 'byline?'

        #In this step we obtain configuration of sample
        
        formcomponent = self.retrieveFormToShow( 'experiment_submission' )
        formcomponent.inventory.id = id
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
            id = id,
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
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page
        
        try:
            self.processFormInputs( director )
        except InputProcessingError, err:
            errors = err.errors
            self.form_received = None
            director.routine = 'submit_experiment'
            return self.submit_experiment( director, errors = errors )

        #make sure experiment is configured all the way
        self._checkstatus(director)
        assert self.allconfigured == True

        # make sure there is a job attached to experiment
        id = self.inventory.id
        experiment = director.clerk.getNeutronExperiment(id)
        jobref = experiment.job
        if not jobref:
            #create new job
            from vnf.components.Job import new_job
            job = new_job(director)
        else:
            job = director.clerk.dereference(jobref)
            
        # establish connections between experiment and job
        job.computation = experiment; director.clerk.updateRecord(job)
        experiment.job = job; director.clerk.updateRecord(experiment)

        # update status of experiment
        experiment.status = 'constructed'
        director.clerk.updateRecord(experiment)

        # redirect to job submission page
        actor = 'neutronexperiment'
        routine = 'view'
        return self.redirect(director, actor, routine, id = id)
        ## --------- obsolete -------
        job = director.clerk.dereference(experiment.job)
        from JobDataManager import JobDataManager
        path = JobDataManager( job, director ).localpath()

        username = director.sentry.username
        if username in ['demo']:
            #demo user can not really run simulation#
            #but they can see a demo
            from NeutronExperimentSimulationRunBuilder_demo import Builder
        else:
            from NeutronExperimentSimulationRunBuilder import Builder
        Builder(path).render(experiment, filedb=director.dss)

        experiment.status = 'constructed'
        director.clerk.updateRecord( experiment )
        
        return self.showExperimentStatus(director)
        ## --------- obsolete -------


    def showExperimentStatus(self,director):
        try:
            page = self._retrievePage(director)
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
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page        

        if self.form_received.submit == 'back':
            return self.start(director)

        return page


    def save_experiment(self, director):
        try:
            page = self._retrievePage(director)
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
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page        

        # remove this experiment
        experiment = director.clerk.getNeutronExperiment(
            self.inventory.id)
        director.clerk.deleteRecord( experiment )

        # go to greeter
        actor = 'neutronexperiment'; routine = 'listall'
        return self.redirect(director, actor, routine)


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


    def _retrievePage(self, director):
#<<<<<<< .mine
#        id = self.getExperimentID(director)
#        experiment = director.clerk.getNeutronExperiment(id)
#        instrument = director.clerk.dereference(experiment.instrument)
#        experiment.sampleassembly = 'polyxtal-fccNi-plate-sampleassembly-0'
#        director.clerk.updateRecord(experiment)
#        if _instrument_without_sample(instrument, director.clerk.db):
#            page = 'neutronexperimentwizard-nosample'
#        else: page = 'neutronexperimentwizard'
#=======
        page = 'neutronexperimentwizard'

        id = self.inventory.id
        if id:
            experiment = director.clerk.getNeutronExperiment(id)
            iref = experiment.instrument
            if iref:
                instrument = director.clerk.dereference(iref)
                if _instrument_without_sample(instrument, director.clerk.db):
                    page = 'neutronexperimentwizard-nosample'
        return director.retrieveSecurePage(page)

    
    def _showstatus(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page

        id = self.inventory.id
        experiment = director.clerk.getNeutronExperiment(id)
        instrument = director.clerk.dereference(experiment.instrument)
        
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
            'instrument_configured': ('configure neutron instrument',
                                      'select_instrument'),
            }
        items = [ 'name_assigned', 'instrument_configured']
        if not _instrument_without_sample(instrument, director.clerk.db):
            d.update( {
                'sample_environment_configured': ('configure sample environment',
                                                  'sample_environment'),
                'sample_prepared': ('prepare a sample',
                                    'sample_preparation'),
                'kernel_configured': ('configure scattering kernel for sample',
                                      'kernel_origin'),
                } )
            items+=[
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

        if instrument_ref:

            instrument = director.clerk.dereference(instrument_ref)
            self.instrument_configured = _instrument_configured(
                experiment, director=director)
            
            if _instrument_without_sample(instrument, director.clerk.db) \
                   and self.instrument_configured:
                
                self.allconfigured = True
                if experiment.status in ['started', 'partially configured']:
                    experiment.status = 'constructed'
                    director.clerk.updateRecord(experiment)
                return

        sampleenvironment_ref = experiment.sampleenvironment
        self.sample_environment_configured = not nullpointer(sampleenvironment_ref)
        
        if self.sample_environment_configured:
            sampleassembly_ref = experiment.sampleassembly
            if not sampleassembly_ref:
                self.sample_prepared = self.kernel_configured = False
            else:
                sampleassembly = director.clerk.dereference(sampleassembly_ref)
                sample = _get_sample_from_sampleassembly(sampleassembly, director.clerk.db)
            
                self.sample_prepared = not nullpointer(sample)
                # need to test if kernel is configured
                # ...
                # probably need a canned solution here for the demo...
                self.kernel_configured = True
            pass

        if not self.kernel_configured: return

        #if experiment.ncount <=0 : return
        #if nullpointer(experiment.job): return
        #job = director.clerk.dereference(experiment.job)

        self.allconfigured = True
        if experiment.status in ['started', 'partially configured']:
            experiment.status = 'constructed'
            director.clerk.updateRecord(experiment)
        return        


    pass # end of NeutronExperimentWizard


def _instrument_configured(experiment, director):
    ic_ref = experiment.instrument_configuration
    if not ic_ref: return False
    ic = director.clerk.dereference(ic_ref)
    return ic.configured


def _instrument_without_sample(instrument, db):
    from vnf.dom.neutron_components.SampleComponent import SampleComponent
    components = instrument.components.dereference(db)
    for name, component in components:
        if isinstance(component, SampleComponent): return False
        continue
    return True


def _get_sample_from_experiment(experiment, db):
    sampleassembly = _get_sampleassembly_from_experiment(experiment, db)
    if not sampleassembly: return
    return _get_sample_from_sampleassembly(sampleassembly, db)


def _get_sample_from_sampleassembly(sampleassembly, db):
    scatterers_refset = sampleassembly.scatterers
    scatterers = scatterers_refset.dereference(db)
    sample = None
    for name, s in scatterers:
        if name == 'sample': sample = s; break
        continue
    return sample


def _get_sampleassembly_from_experiment(experiment, db):
    sampleassembly_ref = experiment.sampleassembly
    if not sampleassembly_ref: return
    return sampleassembly_ref.dereference(db)


def _get_kernels_from_scatterer(scatterer, db):
    kernels_refset = scatterer.kernels
    kernels = kernels_refset.dereference(db)
    return kernels


def _describe_kernel(kernel):
    return '%s: %s' % (kernel.__class__.__name__, kernel.id)


from misc import new_id, empty_id, nullpointer

# version
__id__ = "$Id$"

# End of file 
