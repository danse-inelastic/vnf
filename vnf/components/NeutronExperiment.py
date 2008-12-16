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
from FormActor import FormActor as base


class NeutronExperiment(base):


    class Inventory(base.Inventory):

        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier of the experiment"

        ncount = pyre.inventory.float( 'ncount', default = 1e6 )
        ncount.meta['tip'] = 'number of neutrons'

        pass # end of Inventory


    def default(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperiment' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        # populate the main column
        document = main.document(title='Neutron Experiment')
        document.description = ''
        document.byline = 'byline?'

        p = document.paragraph()
        action = actionRequireAuthentication(
            actor = 'neutronexperimentwizard', sentry = director.sentry,
            label = 'this wizard', routine = 'start',
            )
        wizard_link = action_link( action, director.cgihome )        

        action = actionRequireAuthentication(
            actor = 'neutronexperiment', sentry = director.sentry,
            label = 'experiments', routine = 'listall',
            )
        list_link = action_link( action, director.cgihome )        

        p.text = [
            'In this virtual neutron facility, you can set up',
            'a new experiment by using %s.' % wizard_link,
            'Or you can select from one of the %s you have run' % list_link,
            'and rerun it with new settings.',
            ]
            
        return page


    def delete(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperiment' )
        except AuthenticationError, error:
            return error.page

        record = director.clerk.getNeutronExperiment( self.inventory.id )
        director.clerk.deleteRecord( record )
        return self.listall(director)
        

    def listall(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperiment' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        # populate the main column
        document = main.document(title='Experiments')
        document.description = ''
        document.byline = 'byline?'

        #
        p = document.paragraph()
        action = actionRequireAuthentication(
            label = 'this wizard',
            actor = 'neutronexperimentwizard',
            routine = 'start',
            sentry = director.sentry,
            )
        link = action_link( action, director.cgihome )
        p.text = [
            'You can perform various kinds of neutron experiments in',
            'this virtual neutron facility.',
            'To start, you can plan a new experiment by following %s.' % link,
            ]

        # retrieve id:record dictionary from db
        clerk = director.clerk
        experiments = clerk.indexNeutronExperiments()
        # make a list of all experiments
        listexperiments( experiments.values(), document, director )
        return page


    def view(self, director, id=None):
        try:
            page = director.retrieveSecurePage( 'neutronexperiment' )
        except AuthenticationError, err:
            return err.page

        # the record we are working on
        if id is None: id = self.inventory.id
        else: self.inventory.id = id
        experiment = director.clerk.getNeutronExperiment( id )

        #see if the experiment is constructed or not. if not
        #ask the wizard to do the editing.
        if experiment.status in ['started', 'partially configured']:
            return self.redirect(
                director,
                actor='neutronexperimentwizard',
                routine = 'submit_experiment',
                id = id,
                )

        main = page._body._content._main
        # populate the main column
        document = main.document(
            title='Experiment %r' % experiment.short_description )
        document.description = ( '')
        document.byline = 'byline?'

        status = experiment.status
        method = '_view_%s' % status
        method = getattr(self, method)
        method( document, director )
        return page


    def _obsolete_edit(self, director):
        try:
            page, document = self._head( director )
        except AuthenticationError, error:
            return error.page

        self.processFormInputs( director )

        #see if the experiment is constructed or not. if not
        #ask the wizard to do the editing.
        experiment = director.clerk.getNeutronExperiment( self.inventory.id )
        if experiment.status != 'constructed':
            director.routine = 'start'
            actor = director.retrieveActor( 'neutronexperimentwizard')
            director.configureComponent( actor )
            actor.inventory.id = self.inventory.id
            return actor.start( director )

        formcomponent = self.retrieveFormToShow( 'run_neutron_experiment' )
        formcomponent.inventory.id = self.inventory.id
        formcomponent.director = director
        
        # create form
        form = document.form(
            name='neutronexperiment',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'job', sentry = director.sentry,
            label = '', routine = 'edit',
            arguments = {'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        # run button
        submit = form.control(name="submit", type="submit", value="Run")
            
        return page


    def __init__(self, name=None):
        if name is None:
            name = "neutronexperiment"
        super(NeutronExperiment, self).__init__(name)
        return


    def _view_constructed(self, document, director):
        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        job = director.clerk.dereference(experiment.job)
        
        p = document.paragraph()
        p.text = [
            'Experiment %r has been constructed.' % experiment.short_description,
            ]
        p.text += [
            'Configuration details of this experiment can be',
            'found out in the following tree view.',
            'Please review them before you start the experiment.',
            ]
        
        self._add_review_tree( document, director )
        if job.state in ['created', '']:
            self._add_revision_sentence( document, director )
            self._add_run_sentence( document, director )
        else:
            self._add_view_job_sentence(document, director)
        self._add_delete_sentence( document, director )
        if job.state in ['running']:
            self._add_experiment_output(document, director)
            Scheduler.check(job, director)
        elif job.state in ['finished', 'terminated', 'cancelled']:
            self._add_experiment_results(document, director)
        elif job.state in ['submissionfailed']:
            self._add_resubmit_sentence(document, director)
        return


    def _add_review_tree(self, document, director):
        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        from TreeViewCreator import create
        view = create( experiment, director )
        #view = create( experiment.instrument.dereference(director.clerk.db), director )
        document.contents.append( view )
        return


    def _add_revision_sentence(self, document, director):
        p = document.paragraph()
        action = actionRequireAuthentication(
            label = 'here',
            actor = 'neutronexperimentwizard',
            routine = 'start',
            sentry = director.sentry,
            id = self.inventory.id)
        link = action_link( action, director.cgihome )
        p.text = [
            'If you need to make changes to this experiment,',
            'please click %s.' % link,
            ]
        return


    def _add_run_sentence(self, document, director):
        id = self.inventory.id
        experiment = director.clerk.getNeutronExperiment(id)
        job = experiment.job
        
        p = document.paragraph()
        action = actionRequireAuthentication(
            label = 'here',
            actor = 'job',
            routine = 'view',
            sentry = director.sentry,
            id = job.id)
        link = action_link( action, director.cgihome )
        p.text = [
            'If you are done with experiment configuration,',
            'please click %s to start this experiment as a computation job.' % link,
            ]
        return


    def _add_view_job_sentence(self, document, director):
        id = self.inventory.id
        experiment = director.clerk.getNeutronExperiment(id)
        job = director.clerk.dereference(experiment.job)
        
        p = document.paragraph()
        action = actionRequireAuthentication(
            label = 'here',
            actor = 'job',
            routine = 'view',
            sentry = director.sentry,
            id = job.id)
        link = action_link( action, director.cgihome )
        p.text = [
            'Your experiment was already submitted as a computation job',
            'and the job is %s.' % job.state,
            'Click %s to view the computation job.' % link,
            ]
        return


    def _add_delete_sentence(self, document, director):
        p = document.paragraph()
        action = actionRequireAuthentication(
            label = 'here',
            actor = 'neutronexperiment',
            routine = 'delete',
            sentry = director.sentry,
            id = self.inventory.id)
        link = action_link( action, director.cgihome )
        p.text = [
            'To delete this experiment, please click %s.' % link,
            ]
        return
    

    def _add_resubmit_sentence(self, document, director):
        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        
        p = document.paragraph( )
        p.text = [
            'We have tried to start experiment %r for you but failed.' % experiment.short_description,
            'This could be due to network error.',
            'The error message returned from computation server is:',
            ]

        job = director.clerk.dereference(experiment.job)
        
        p = document.paragraph(cls = 'error'  )
        p.text = [ job.error ]

        p = document.paragraph()
        action = actionRequireAuthentication(
            label = 'resubmit',
            actor = 'job',
            routine = 'edit',
            sentry = director.sentry,
            id = job.id)
        link = action_link( action, director.cgihome )
        p.text = [
            'If you are sure that the error was fixed, please %s' % link,
            ]
        return 


    def _add_experiment_output(self, document, director):
        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        job = director.clerk.dereference(experiment.job)
        server = director.clerk.dereference(job.server)
        instrument = director.clerk.dereference(experiment.instrument)

        #refresh script
        import vnf.content
        autorefresh = vnf.content.autorefresh(timeout=10)
        document.contents.append(autorefresh)

        # experimental outputs
        panel = document.form(
            name='null',
            legend= 'Summary',
            action='')
        p = panel.paragraph()
        p.text = [
            'Experiment %r was started %s on server %r, using %s nodes.' % (
            experiment.short_description, job.time_start,
            server.short_description,
            job.numprocessors,
            ),
            ]

        # data display
        datadisplay = document.form(
            name='null',
            legend= 'Data',
            action='')

        # loop over components and make display
        from vnf.dom.neutron_components.Monitor import Monitor
        for name, component in \
                director.clerk.dereference(instrument.components):

            # skip non monitors
            if not isinstance(component, Monitor): continue
            
            self._display_component_output(
                name, component, datadisplay, director)
        return


    def _add_experiment_results(self, document, director):
        # ******** needs update
        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        job = director.clerk.dereference(experiment.job)
        server = director.clerk.dereference(job.server)
        instrument = director.clerk.dereference(experiment.instrument)

        panel = document.form(
            name='null',
            legend= 'Experiment outputs',
            action='')

        job = director.clerk.dereference(experiment.job)

        # loop over components and make display
        from vnf.dom.neutron_components.Monitor import Monitor
        for name, component in \
                director.clerk.dereference(instrument.components):
            
            # skip non monitors
            if not isinstance(component, Monitor): continue
            
            self._display_component_output(
                name, component, panel, director)

        return


    def _display_component_output(self, name, component, document, director):
        # output file name
        from vnf.components.job_builders.NeutronExperiment import outputfiles
        component.label = name
        paths = outputfiles(component)

        # sync file from computation server
        id = self.inventory.id
        experiment = director.clerk.getNeutronExperiment(id)
        job = director.clerk.dereference(experiment.job)
        self._sync(job, paths, director)

        #
        viewname = component.__class__.__name__.lower()
        self._retrieveView(
            viewname, director,
            datafiles = [director.dds.abspath(job, path) for path in paths],
            document = document,
            )
        return

    
    def _sync(self, job, filenames, director):
        # should check if the file in the remote job directory is newer than
        # the local job directory
        # current implementation does not check for that...
        dds = director.dds
        server = director.clerk.dereference(job.server)

        for filename in filenames:
            # if the file has not been generated, skip
            if not dds.is_available(job, filename=filename, server=server): return

            path = dds.abspath(job, filename=filename)
            import os
            if os.path.exists(path):
                # remove the local copy
                os.remove(path)
                # let dds forget the local copy
                dds.forget(job, filename=filename)

            # check if it exists in the server
            if not dds.is_available(job, filename=filename, server=server):
                # if not, skip
                continue
            # let dds know that it exists in the server
            #dds.remember(job, filename=filename, server=server)
            # make it available locally
            dds.make_available(job, files=[filename])
            continue
        
        return


    def _retrieveView(self, name, director, **kwds):
        view = director.retrieveComponent(
            name,
            factory='view',
            args=[kwds],
            vault=['views/neutron_component_outputs'],
            )
        return view


    def _configure(self):
        base._configure(self)
        self.id = self.inventory.id
        return


    pass # end of NeutronExperiment



from wording import plural, present_be

def listexperiments( experiments, document, director ):

    n = len(experiments)
    if not n: return
    
    p = document.paragraph()
    p.text = [ 'Here is a list of experiments you have planned or run:' ]


    formatstr = '%(index)s: %(viewlink)s (%(status)s) is a measurement of %(sample)r in %(instrument)r (%(deletelink)s)'
    actor = 'neutronexperiment'
    container = experiments

    for i, element in enumerate( container ):
        
        p = document.paragraph()
        name = element.short_description
        if name in ['', None, 'None'] : name = 'undefined'
        action = actionRequireAuthentication(
            actor, director.sentry,
            routine = 'view',
            label = '%s(%s)' % (element.id, name),
            id = element.id,
            )
        viewlink = action_link( action,  director.cgihome )

        action = actionRequireAuthentication(
            actor, director.sentry,
            routine = 'delete',
            label = 'delete',
            id = element.id,
            )
        deletelink = action_link( action,  director.cgihome )

        if nullpointer(element.instrument) :
            action = actionRequireAuthentication(
                'neutronexperimentwizard', sentry = director.sentry,
                label = 'select instrument',
                routine = 'select_instrument',
                id = element.id,
                )
            link = action_link( action, director.cgihome )
            instrument = link
        else:
            instrument = director.clerk.dereference(element.instrument)
            instrument = instrument.short_description
            pass # end if
        
        subs = {'index': i+1,
                'viewlink': viewlink,
                'deletelink': deletelink,
                'status': element.status,
                'instrument': instrument,
                'sample': 'sample',
                }

        p.text += [
            formatstr % subs,
            ]
        continue
    return


def view_instrument(instrument, form):
    p = form.paragraph()
    p.text = [
        'This experiment is to be performed in instrument %s' % instrument.short_description,
        ]
    
    from TreeViewCreator import create
    view = create( instrument )
    form.contents.append( view )
    return


def view_sampleassembly(sampleassembly, form):
    p = form.paragraph()
    p.text = [
        'The sample to study: %s' % sampleassembly.short_description,
        ]

    from TreeViewCreator import create
    view = create( sampleassembly )
    form.contents.append( view )
    return


def view_instrument_plain(instrument, form):
    p = form.paragraph()
    p.text = [
        'This experiment is to be performed in instrument %s' % instrument.short_description,
        ]
    
    p = form.paragraph()
    geometer = instrument.geometer
    components = instrument.componentsequence
    p.text = [
        'Instrument %r has %s components: %s' % (
        instrument.short_description, len(components),
        ', '.join( [ comp for comp in components ] ) ),
        ]
    
    excluded_cols = [
        'id', 'creator', 'date', 'short_description',
        ]
    p = form.paragraph()
    p.text = [ '<UL>' ]
    for component in components:
        if component != 'sample': 
            component_record = getattr( instrument, component ).realcomponent
            component_type = component_record.__class__.__name__
        else:
            component_type = ''
            pass # endif
        p.text.append( '<li>%s: %s' % (component, component_type) )
        p.text.append( '<UL>' )
        record = geometer[ component ]
        p.text.append( '<li>Position: %s' % (record.position,) )
        p.text.append( '<li>Orientation: %s' % (record.orientation,) )
        
        if component == 'sample':
            p.text.append( '</UL>' )
            continue
        
        columns = component_record.getColumnNames()
        for col in columns:
            if col in excluded_cols: continue
            value = getattr( component_record, col )
            p.text.append('<li>%s: %s' % (col, value) )
            continue
        
        p.text.append( '</UL>' )
        continue
    p.text.append( '</UL>' )
    return


class ResultDrawer:

    def draw(self, experiment, result, document, director):
        #special place to save plots
        plots_path = 'images/plots'

        #
        results = director.clerk.getSimulationResults( experiment )
        labels = [ r.label for r in results ]

        if result in labels:
            #if result already saved, just fetch that
            id = filter( lambda r: r.label == result, results )[0].id
        else:
            #otherwise, we need to have a new record in simulatoinresults table
            #and also need to save result in the special place
            src = result
            #simulationresults record
            from vnf.dom.SimulationResult import SimulationResult
            result_record = director.clerk.newDbObject(SimulationResult)
            result_record.label = result
            result_record.simulation_type = 'NeutronExperiment'
            result_record.simulation_id = experiment.id
            director.clerk.updateRecord( result_record )

            id = result_record.id
            # copy file to a special place
            filepath1 = os.path.join( plots_path, '%s.png' % id )
            dest = os.path.join( 'html', filepath1 )
            #copy
            import shutil
            shutil.copyfile( src, dest )
            
        filepath1 = os.path.join( plots_path, '%s.png' % id )
            
        #create view
        #hack
        path, name = os.path.split( result )
        name, ext = os.path.splitext( name )
        p = document.paragraph()
        p.text = [
            name,
            ]
        p = document.paragraph()
        p.text = [
            '<img src="%s/%s">' % ( director.home, filepath1 ),
            ]
        return


#switch pylab backend to ps so that it does not need interactivity
import os, spawn
import Scheduler

from misc import empty_id, nullpointer

# version
__id__ = "$Id$"

# End of file 
