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


from Actor import action_link, action, actionRequireAuthentication, AuthenticationError
from wording import plural, present_be


from FormActor import FormActor as base


class Job(base):

    class Inventory(base.Inventory):

        import time
        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier for a given search"


    def default(self, director):
        return self.listall( director )


    def listall(self, director):
        page = director.retrievePage( 'job' )
        
        main = page._body._content._main
        
        # populate the main column
        document = main.document(title='List of computational jobs')
        document.description = ''
        document.byline = 'byline?'

        # retrieve id:record dictionary from db
        clerk = director.clerk
        jobs = clerk.getJobs( where = 'owner=%r' % director.sentry.username )
            
        p = document.paragraph()

        numJobs = len(jobs)

        columns = [
            'jobName', 'id', 'owner', 'server',
            'numprocessors', 'status', 'timeStart', 'timeCompletion',
            ]
        numColumns=len(columns)

        from PyHtmlTable import PyHtmlTable
        t=PyHtmlTable(numJobs,numColumns, {'width':'400','border':2,'bgcolor':'white'})
        for colNum, col in enumerate(columns):
            t.setc(0,colNum,col)
            continue
        
        for row, job in enumerate( jobs ):
            for colNum, colName in enumerate( columns ):
                
                value = job.getColumnValue(colName)
                if colName == 'jobName':
                    link = action_link(
                        actionRequireAuthentication(
                        'job',
                        director.sentry,
                        label = value,
                        routine = 'show',
                        id = job.id,
                        ),  director.cgihome
                        )
                    value = link
                    pass # endif
                        
                t.setc(row+1,colNum,value)
                #colNum+=1
        p.text = [t.return_html()]
        
        return page


    def edit(self, director):
        try:
            page = director.retrieveSecurePage( 'job' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        job = self.processFormInputs( director )
        if job is None: # input is not from form
            job = director.clerk.getJob( self.inventory.id )
            pass # endif
        
        document = main.document( title = 'Job editor' )

        formcomponent = self.retrieveFormToShow( 'job' )
        formcomponent.inventory.id = job.id
        formcomponent.director = director

        form = document.form(
            name='job',
            legend = formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'job', sentry = director.sentry,
            label = '', routine = 'submit',
            arguments = {'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        submit = form.control(name="submit", type="submit", value="Submit")
        
        return page


    def show(self, director):
        try:
            page = director.retrieveSecurePage( 'job' )
        except AuthenticationError, err:
            return err.page
        
        id = self.inventory.id
        record = director.clerk.getJob( id )
        assert record.owner == director.sentry.username

        main = page._body._content._main
        document = main.document( title = 'Job # %s: %s' % (
            record.id, record.status ) )

        if record.status == 'created':
            p = document.paragraph()
            link = action_link(
                actionRequireAuthentication(
                'job',
                director.sentry,
                label = 'submit',
                routine = 'edit',
                id = record.id,
                ),  director.cgihome
                )
            
            p.text = [
                'This job is created but not submitted.',
                'Please %s it first' % link,
                ]
            return page
            
        if record.status not in ['created', 'finished']:
            status = check( record, director )

        props = record.getColumnNames()
        lines = ['%s=%s' % (prop, getattr(record, prop) ) for prop in props]
        for line in lines:
            p = document.paragraph()
            p.text = [line]
            continue
        return page


    def submit(self, director):
        try:
            page = director.retrieveSecurePage( 'job' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        job = self.processFormInputs( director )

        server = job.server
        server_record = director.clerk.getServer( server )

        try:
            schedule(job, director)
        except Exception, err:
            import traceback
            self._debug.log( traceback.format_exc() )
            document = main.document( title = 'Job not submitted' )
            p = document.paragraph()
            p.text = [
                'Failed to submit job %s to %s' % (
                job.id, server_record.server, ),
                ]
            return page

        job.status = 'submitted'
        director.clerk.updateRecord( job )
        # check status of job
        check( job, director )
        
        document = main.document( title = 'Job submitted' )
        p = document.paragraph()
        p.text = [
            'Job #%s has been submitted to %s' % (
            job.id, server_record.server, ),
            ]
            
        p = document.paragraph()
        p.text = [
            'You can click "Jobs" link on the left menu to see all of your jobs',
            ]
            
        return page


    def __init__(self, name=None):
        if name is None:
            name = "job"
        super(Job, self).__init__(name)
        return


from Scheduler import schedule, check, RemoteAccessError


def new_job( director ):
    job = new_job_record( director )
    #create local directory for job
    data_manager(job, director).initlocaldir()
    return job
    

def data_manager( job, director ):
    from JobDataManager import JobDataManager
    return JobDataManager(job, director)


def new_job_record( director ):
    id = new_jobid( director )
    from vnf.dom.Job import Job
    job = Job()
    job.id = id
    director.clerk.newJob( job )

    job.owner = director.sentry.username
    job.status = 'created'
    job.exit_code = -1
    import time
    job.timeStart = job.timeCompletion = time.ctime()

    servers = director.clerk.getServers()
    server = servers[0]
    job.server = server.id

    job.numprocessors = 1
    
    return job


from misc import new_id as new_jobid



# version
__id__ = "$Id$"

# End of file 
