# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

"""
base actor class for simple arcs applications

Note:
 * an actor must collaborate with a visual factory. both of them should
   be assigned the same name
""" 

import luban.content


# The action to load the job-editor panel
# select(id='main-display-area').replaceContent(...)
loadjobeditor = lambda id: luban.content.load(
    actor='job', 
    routine='view',
    id = id,
    )
        

from luban.components.AuthorizedActor import AuthorizedReceptionist as base
class AppActorBase(base):

    ormactorname = None
    tablename = None

    class Inventory(base.Inventory):

        import pyre.inventory

        id = pyre.inventory.str('id')
        
        formids = pyre.inventory.list('formids')
        viewid = pyre.inventory.str('viewid')

        histogram = pyre.inventory.str('histogram')

        name = pyre.inventory.str('name')
        method = pyre.inventory.str('method', default='build')


    def showTable(self, director):
        vf = self._visualFactory(director)
        workpanel = luban.content.select(id=vf.start_panel.workpanelid)
        tableview = luban.content.load(
            actor=self.tableactorname, 
            routine='createListView')
        return workpanel.replaceContent(tableview)


    def view(self, director):
        """view one computation
        """
        title = self._createViewTitle(director)
        doc = luban.content.document(title=title)
        
        sp = luban.content.splitter(); doc.add(sp)
        propsdoc = director.redirect(
            actor=self.ormactorname,
            routine = 'displayProperties',
            id = self.inventory.id,
            editlink=False,
            include_credential=False,
            )
        sp.section().add(propsdoc)
        
        v = self.createView(director)
        sp.section().add(v)
        
        vf = self._visualFactory(director)
        workpanelid = vf.start_panel.workpanelid
        return luban.content.select(id=workpanelid).replaceContent(doc)


    def update(self, director):
        """update view of the given computation.
        
        This routine is triggered when user click the "update"
        button. It means user input has been saved to the database
        as a record, and user wants to see the corresponding result
        for the simulation. 
        What is going to be done here is
        
        * make sure user already submit the simulation parameter
        * check if the simulation user wants to run is already run
        * if yes, show the result if it is available, otherwise show the result retrieval process
        * if not, prepare the job submission form

        inputs:
        * id: id of the computation
        """
        
        # check if there are unfilled forms
        actions = self._checkForms(director)
        if actions: return actions
        
        # check if we have results, if yes, show them
        if self._hasResults(director):
            return self.showResults(director)

        # if no result but job is done, get the results
        if self._jobIsDone(director):
            return self.getResults(director)
        
        # job is not done, prepare a job for the simulation
        return self.prepareSimulation(director)
    
    
    def _createViewTitle(self, director):
        """return title for the view of one computation"""
        raise NotImplementedError
        return 'ARCS IQE resolution computation #%s' % self.inventory.id
        

    def showResults(self, director):
        """show the results of the simulation
        """
        doc = self.createView(director)
        return luban.content.select(id='main-display-area').replaceContent(doc)
    
    
    def downloadHistogram(self, director):
        """return download data stream for the given histogram

        inputs:
        * id: id of the computation
        * histogram: the histogram file path inside the computation directory
        """
        id = self.inventory.id
        dds = director.dds
        domaccess = director.retrieveDOMAccessor('computation')
        computation = domaccess.getComputationRecord(
            self.tablename, id)

        # read data
        histogram = self.inventory.histogram
        p = dds.abspath(computation, histogram)
        content = open(p, 'rb').read()
        
        # file base name
        import os
        basename = os.path.basename(histogram)
        
        #
        return luban.content.file(filename=basename, content=content)
    
    
    def createView(self, director):
        """create the view of the simulation

        inputs:
        * id: id of the simulation
        """
        
        # check if we have results, if yes, show them
        if self._hasResults(director):
            vfroot = self._visualFactory(director)
            vf = vfroot.results_view
            return vf.build(id=self.inventory.id)
        
        # the view 
        doc = luban.content.document(id='main-display-area')

        #
        id = self.inventory.id
        computation = self._getComputation(director)
        # if job is done, show the computation result retrieval view
        if self._jobIsDone(director):
            # when results are retrieved, load this actor
            on_all_results_retrieved = "load(actor=%r, routine='update', id=%r)" % (
                self.name, id)
            vis = director.retrieveVisual(
                'computation-results',
                computation=computation,
                actor='computation', 
                on_all_results_retrieved = on_all_results_retrieved,
                director=director,
                )
        else:
            # otherwise, the job status view
            vis = self.createJobStatusView(director)
        
        #
        doc.add(vis)
        return doc


    def getResults(self, director):
        """display the view of getting results
        """
        raise NotImplementedError
    
    
    def prepareSimulation(self, director):
        """if the computation already has a job running/finished/etc, will show job status
        otherwise, present the view to edit and submit the job
        """
        # load the computation from db
        computation = self._getComputation(director)
        
        # if there is already a job, just present it
        job = computation.getJob(director.clerk.db)
        if job: 
            return self.presentJobStatus(director)

        job = self._createJob(director, computation=computation)
        
        return loadjobeditor(job.id)


    def _createJob(self, director, computation=None):
        """create job for the given computation
        """
        # load the computation from db
        computation = computation or self._getComputation(director)
        
        job = computation.getJob(director.clerk.db)
        if job: 
            raise RuntimeError, "should not reach here: job already exists. computation: %s, job: %s" % (computation.id, job.id)
        
        # create new job
        from vnf.utils.job import new
        job = new(director)
        
        # assign computation
        job.computation = computation
        
        # update
        director.clerk.updateRecordWithID(job)
        
        return job

    
    def createJobStatusView(self, director):
        """create job status view
        """
        # load the computation from db
        computation = self._getComputation(director)
        
        # there should be a job already
        job = computation.getJob(director.clerk.db)
        if not job: 
            raise RuntimeError, "should not reach here: job does not exist. computation: %s" % (computation.id, )

        #
        doc = luban.content.document()
        text = [
            'There is a computation job for this simulation. ',
            'It is now %s' % job.state,
            ]
        doc.paragraph(text=text)
        
        link = luban.content.link(label='View the job details', onclick=loadjobeditor(job.id))
        doc.add(link)

        return doc

    
    def presentJobStatus(self, director):
        """display the job status view
        """
        doc = self.createJobStatusView(director)
        return luban.content.select(id='main-display-area').replaceContent(doc)

    
    def _hasResults(self, director):
        """check if results are available for the computation
        """
        raise NotImplementedError


    def _jobIsDone(self, director):
        """check if job is done for the given computation"""
        raise NotImplementedError


    def _getComputation(self, director):
        """load the computation from db"""
        raise NotImplementedError
    

    def _checkForms(self, director):
        """check forms and alert if there are not-yet-submitted forms"""
        actions = []; messages = []
        formids = self.inventory.formids
        actions += [luban.content.select(id=id).addClass('highlighted') for id in formids]
        n = len(formids)
        if n > 1:
            msg = 'sorry. there are %s forms to submit.' % n
        else:
            msg = 'sorry. there is a form to submit.'
        msg += 'Please look for highlighted sections.'
        messages.append(msg)
        
        if len(actions):
            actions.append(luban.content.alert('\n\n'.join(messages)))
            return actions


    def _visualFactory(self, director):
        """create visual factory"""
        raise NotImplementedError


    def loadVisual(self, director):
        """load a visual factory and use it to build the visual, and return it

        inputs:
        * name: name of the factory w.r.t the visual factory root
          e.g. to load a visual factory "results_view', name='results_view'
        * method: name of the method of the factory to be called 
        * other inputs, will be fed to the method of the visual factory
          to build the visual
        """
        
        # get visual factory
        vfroot = self._visualFactory(director)
        def _getattr(obj, name):
            if name.find('.') == -1:
                return getattr(obj, name)
            tokens = name.split('.')
            o1 = getattr(obj, tokens[0])
            return _getattr(o1, tokens[1:])
        vf = _getattr(vfroot, self.inventory.name)

        # method
        method = getattr(vf, self.inventory.method)

        # build visual
        kwds = {}
        # the attributes in inventory
        props = self.inventory.properties()
        props = [p for p in props if p not in self.inventory.facilities()]
        for prop in props:
            name = prop.name
            if name.startswith('help-'): continue
            value = prop.__get__(self.inventory)
            kwds[name] = value
            continue
        # the attributes outside of inventory
        for k, v in self.inventory.__dict__.iteritems():
            if k.startswith('_'): continue
            if hasattr(self.Inventory, k): continue
            kwds[k] = v
            continue
        return method(**kwds)
    

    def __init__(self, name=None, tableactorname=None):
        super(AppActorBase, self).__init__(name)
        
        # the actor to handle table view
        self.tableactorname = tableactorname or (name + 's')
        return


# version
__id__ = "$Id: __init__.py 3677 2011-03-31 22:12:33Z linjiao $"

# End of file 
