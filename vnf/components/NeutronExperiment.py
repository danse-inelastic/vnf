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
        director.clerk.deleteExperiment( record )
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
        where = "creator='%s' and status!='deleted'" % director.sentry.username
        experiments = clerk.indexNeutronExperiments(where=where)
        # make a list of all experiments
        listexperiments( experiments.values(), document, director )
        return page


    def view(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperiment' )
        except AuthenticationError, err:
            return err.page

        # the record we are working on
        id = self.inventory.id
        experiment = director.clerk.getNeutronExperiment( id )

        #see if the experiment is constructed or not. if not
        #ask the wizard to do the editing.
        if experiment.status in ['started', 'partially configured', 'ready for submission']:
            return director.redirect(
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

        status = experiment.status.replace(' ', '_')
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

    document.contents.append(experimenttable(experiments, director))
    return


def experimenttable(experiments, director):
    from vnf.content.table import Model, View, Table
    class model(Model):

        id = Model.Measure(name='id', type='text')
        description = Model.Measure(name='description', type='text')
        sample = Model.Measure(name='sample', type='text')
        instrument = Model.Measure(name='instrument', type='text')


    def getDesc(exp):
        label = exp.short_description or exp.id
        action = actionRequireAuthentication(
            sentry = director.sentry,
            label = label,
            actor = 'neutronexperiment',
            routine = 'view',
            id = exp.id,
            )
        return action_link(action, director.cgihome)
    def getSample(exp):
        from NeutronExperimentWizard import _get_sample_from_experiment
        sample = _get_sample_from_experiment(exp, director.clerk.db)
        if not sample: return 'not defined'
        label = sample.short_description or sample.chemical_formula
        return label
    def getInstrument(exp):
        instrument_ref = exp.instrument
        if not instrument_ref: return "not defined"
        instrument = director.clerk.dereference(instrument_ref)
        label = instrument.short_description
        action = actionRequireAuthentication(
            sentry = director.sentry,
            label = label,
            actor = 'instrument',
            routine = 'show',
            id = instrument.id,
            )
        link = action_link(action, director.cgihome)
        return link
        
    import operator
    generators = {
        'id': operator.attrgetter('id'),
        'description': getDesc,
        'sample': getSample,
        'instrument': getInstrument,
        }
    
    class D: pass
    def d(s):
        r = D()
        for attr, g in generators.iteritems():
            value = g(s)
            setattr(r, attr, value)
            continue
        return r
    data = [d(e) for e in experiments]

    class view(View):
        
        columns = [
            View.Column(id='col1',label='ID', measure='id'),
            View.Column(id='col2',label='Description', measure='description'),
            View.Column(id='col3',label='Sample', measure='sample'),
            View.Column(id='col4',label='Instrument', measure='instrument'),
            ]

        editable = False

    table = Table(model, data, view)
    return table


def view_sampleassembly(sampleassembly, form):
    p = form.paragraph()
    p.text = [
        'The sample to study: %s' % sampleassembly.short_description,
        ]

    from TreeViewCreator import create
    view = create( sampleassembly )
    form.contents.append( view )
    return


import os
import Scheduler

from misc import nullpointer

# version
__id__ = "$Id$"

# End of file 
