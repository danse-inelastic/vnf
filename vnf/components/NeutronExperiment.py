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
        if experiment.status in ['started', 'partially configured']:
            director.routine = 'submit_experiment'
            actor = director.retrieveActor( 'neutronexperimentwizard')
            director.configureComponent( actor )
            actor.inventory.id = self.inventory.id
            return actor.submit_experiment( director )

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


    def edit(self, director):
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


    def run(self, director):
        try:
            page = director.retrieveSecurePage( 'neutronexperiment' )
        except AuthenticationError, err:
            return err.page

        experiment = director.clerk.getNeutronExperiment(
            self.inventory.id)
        job_id = experiment.job_id
        if empty_id(job_id):
            raise RuntimeError, "job not yet established"
        
        job_id  = experiment.job_id
        job = director.clerk.getJob( job_id )
        
        try:
            Scheduler.schedule(job, director)
            experiment.status = 'submitted'
        except Exception, err:
            raise
            import traceback
            experiment.status = 'submissionfailed'
            job.error = traceback.format_exc()

        # update db
        director.clerk.updateRecord( job )
        director.clerk.updateRecord( experiment )
        
        # check status of job
        Scheduler.check( job, director )

        return self.view( director )


    def selectinstrument(self, director):
        try:
            page, document = self._head( director )
        except AuthenticationError, error:
            return error.page

        experiment = director.clerk.getNeutronExperiment(
            self.inventory.id )
        
        # create form to set scatterer type
        formcomponent = self.retrieveFormToShow( 'selectneutroninstrument' )
        formcomponent.inventory.experiment_id = experiment.id
        formcomponent.director = director
        
        # create form
        form = document.form(
            name='selectneutroninstrument',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'neutronexperiment', sentry = director.sentry,
            label = '', routine = 'edit',
            arguments = { 'id': experiment.id,
                          'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        # ok button
        submit = form.control(name="submit", type="submit", value="OK")
        
        return page


    def __init__(self, name=None):
        if name is None:
            name = "neutronexperiment"
        super(NeutronExperiment, self).__init__(name)
        return


    def _add_review(self, document, director):
        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        experiment = director.clerk.getHierarchy( experiment )
        from TreeViewCreator import create
        view = create( experiment )
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
        p = document.paragraph()
        action = actionRequireAuthentication(
            label = 'here',
            actor = 'neutronexperiment',
            routine = 'run',
            sentry = director.sentry,
            id = self.inventory.id)
        link = action_link( action, director.cgihome )
        p.text = [
            'If you are done with experiment configuration,',
            'please click %s to start this experiment.' % link,
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
    

    def _view_constructed(self, document, director):
        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        p = document.paragraph()
        p.text = [
            'Experiment %r has been constructed.' % experiment.short_description,
            ]
        p.text += [
            'Configuration details of this experiment can be',
            'found out in the following tree view.',
            'Please review them before you start the experiment.',
            ]

        self._add_review( document, director )
        self._add_revision_sentence( document, director )
        self._add_run_sentence( document, director )
        self._add_delete_sentence( document, director )
        return


    def _view_submissionfailed(self, document, director):
        p = document.paragraph( )
        p.text = [
            'We have tried to start experiment %r for you but failed.' % experiment.short_description,
            'This could be due to network error.',
            'The error message returned from computation server is:',
            ]

        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        experiment = director.clerk.getHierarchy( experiment )
        p = document.paragraph(cls = 'error'  )
        p.text = [ experiment.job.error ]

        p = document.paragraph()
        p.text += [
            'Configuration details of this experiment can be',
            'found out in the following tree view.',
            ]

        self._add_review( document, director )
        self._add_revision_sentence( document, director )
        self._add_run_sentence( document, director )
        self._add_delete_sentence( document, director )
        return 


    def _view_submitted(self, document, director):
        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        experiment = director.clerk.getHierarchy( experiment )

        #refresh script
        p = document.paragraph()
        p.text = [
            '''
        <script>
        <!--

        /*
        Auto Refresh Page with Time script
        By JavaScript Kit (javascriptkit.com)
        Over 200+ free scripts here!
        */

        //enter refresh time in "minutes:seconds" Minutes should range from 0 to inifinity. Seconds should range from 0 to 59
        var limit="0:10"

        var parselimit=limit.split(":")
        parselimit=parselimit[0]*60+parselimit[1]*1

        function beginrefresh(){
            if (parselimit==1)
            window.location.reload()
            else{
            parselimit-=1
            curmin=Math.floor(parselimit/60)
            cursec=parselimit%60
            if (curmin!=0)
            curtime=curmin+" minutes and "+cursec+" seconds left until page refresh!"
            else
        curtime=cursec+" seconds left until page refresh!"
        window.status=curtime
        setTimeout("beginrefresh()",1000)
        }
        }

        window.onload=beginrefresh
        //-->
        </script>
        ''',
            ]
        
        panel = document.form(
            name='null',
            legend= 'Summary',
            action='')
            
        p = panel.paragraph()
        p.text = [
            'Experiment %r was started %s on server %r, using %s nodes.' % (
            experiment.short_description, experiment.job.timeStart,
            experiment.job.computation_server.short_description,
            experiment.job.numprocessors,
            ),
            ]
        p.text += [
            'Configuration details of this experiment can be',
            'found out in the following tree view.',
            ]
        self._add_review( panel, director )
        self._add_results( document, director )

        #update status
        if experiment.job.status == 'finished': experiment.status = 'finished'
        director.clerk.updateRecord( experiment )
        return


    def _view_finished(self, document, director):
        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        experiment = director.clerk.getHierarchy( experiment )

        panel = document.form(
            name='null',
            legend= 'Summary',
            action='')
            
        p = panel.paragraph()
        p.text = [
            'Experiment %r was started %s on server %r, using %s nodes.' % (
            experiment.short_description, experiment.job.timeStart,
            experiment.job.computation_server.short_description,
            experiment.job.numprocessors,
            ),
            ]
        p.text += [
            'Configuration details of this experiment can be',
            'found out in the following tree view.',
            ]
        self._add_review( panel, director )
        self._add_results( document, director )

        #update status
        if experiment.job.status == 'finished': experiment.status = 'finished'
        director.clerk.updateRecord( experiment )
        return


    def _add_results(self, document, director):
        experiment = director.clerk.getNeutronExperiment( self.inventory.id )

        # data path
        job_id = experiment.job_id
        job = director.clerk.getJob( job_id )
        
        from JobDataManager import JobDataManager
        jobdatamanager = JobDataManager( job, director )
        
        path = jobdatamanager.localpath()
        server = job.computation_server

        # list entries in the job directory in the remote server
        output_files = jobdatamanager.listremotejobdir()

        document = document.form(
            name='null',
            legend= 'Data',
            action='')
        
        # loop over expected results and see if any of them is available
        # and post it
        expected = experiment.expected_results
        import os
        for item in expected:
            filename = item
            if filename in output_files:
                #f = os.path.join( path, item )
                #retieve file from computation server
                localcopy = jobdatamanager.makelocalcopy( filename )
                self._post_result( localcopy, document, director )
            continue
        return


    def _post_result(self, resultfile, document, director):
        drawer = ResultDrawer( )
        experiment = director.clerk.getNeutronExperiment( self.inventory.id )
        drawer.draw( experiment, resultfile, document, director )
        return


    def _head(self, director):
        page = director.retrieveSecurePage( 'neutronexperiment' )
        
        main = page._body._content._main

        # the record we are working on
        id = self.inventory.id
        experiment = director.clerk.getNeutronExperiment( id )

        # populate the main column
        document = main.document(
            title='Neutron Experiment: %s' % experiment.short_description )
        document.description = ( '')
        document.byline = '<a href="http://danse.us">DANSE</a>'

        return page, document


    def _configure(self):
        base._configure(self)
        self.id = self.inventory.id
        return


    pass # end of NeutronExperiment



from wording import plural, present_be

def listexperiments( experiments, document, director ):
    p = document.paragraph()

    n = len(experiments)

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
            label = name,
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

        element = director.clerk.getHierarchy( element )
        if element.instrument is None \
               or element.instrument.instrument is None:
            action = actionRequireAuthentication(
                'neutronexperimentwizard', sentry = director.sentry,
                label = 'select instrument',
                routine = 'select_instrument',
                id = element.id,
                )
            link = action_link( action, director.cgihome )
            instrument = link
        else:
            instrument = element.instrument.instrument
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
            result_record = director.clerk.new_dbobject(SimulationResult)
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

from misc import empty_id

# version
__id__ = "$Id$"

# End of file 
