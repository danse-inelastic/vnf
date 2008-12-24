#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Actor import AuthenticationError, actionRequireAuthentication
from FormActor import FormActor

class SampleInput(FormActor):

    class Inventory(FormActor.Inventory):

        import pyre.inventory

        sampleId = pyre.inventory.str("id", default=None)
        sampleId.meta['tip'] = "the unique identifier for a given sample"
        
        matterId = pyre.inventory.str("id", default=None)
        matterId.meta['tip'] = "the unique identifier for a given material"
        
        sampleId = pyre.inventory.str("id", default=None)
        sampleId.meta['tip'] = "the unique identifier for a given sample shape"
        
        page = pyre.inventory.str('page', default='empty')

    def default(self, director):
        return self.inputMaterial(director)
    
    def inputMaterialType(self, director):
        try:
            page = director.retrievePage( 'generic' )
        except AuthenticationError, err:
            return err.page
        
#        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        main = page._body._content._main
        # populate the main column
        document = main.document(title='Material type input')
        document.description = ''
        document.byline = '<a href="http://danse.us">DANSE</a>'        
        
        formcomponent = self.retrieveFormToShow('inputMaterialType')
        formcomponent.director = director
        # build the form 
        form = document.form(name='', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'sampleInput', 
            sentry = director.sentry,
            routine = 'chooseMaterialInputForm',
            label = '',
            id=self.inventory.id,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        submit = form.control(name='submit',type="submit", value="next")
        return page  
    
    def chooseMaterialInputForm(self, director):
        selected = self.processFormInputs(director)
        method = getattr(self, selected )
        return method( director )
        
    def inputMaterial(self, director):
        try:
            page = director.retrievePage( 'generic' )
        except AuthenticationError, err:
            return err.page
        
        matter = self._createMatter(director)
        matterId = pyre.inventory.str("id", default=None)
        matterId.meta['tip'] = "the unique identifier for a given material"
        matterid = self.inventory.matterId = matter.
        
#        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        main = page._body._content._main
        # populate the main column
        document = main.document(title='Material input')
        document.description = ''
        document.byline = '<a href="http://danse.us">DANSE</a>'        
        
        formcomponent = self.retrieveFormToShow('inputMaterial')
        formcomponent.director = director
        # build the form 
        form = document.form(name='', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'sampleInput', 
            sentry = director.sentry,
            routine = 'storeAndVerifyInput',
            label = '',
            id=self.inventory.id,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        submit = form.control(name='submit',type="submit", value="next")
        return page  
    
    def storeAndVerifyInput(self, director):
        try:
            page = self._retrievePage(director)
        except AuthenticationError, err:
            return err.page
        self.processFormInputs(director) 
        return self.selectShape( director ) 
    
    def selectShape(self, director):
        try:
            page = director.retrieveSecurePage( 'generic' )
        except AuthenticationError, err:
            return err.page
#        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        main = page._body._content._main
        # populate the main column
        document = main.document(title='Shape input')
        document.description = ''
        document.byline = '<a href="http://danse.us">DANSE</a>'        
        
        formcomponent = self.retrieveFormToShow( 'selectShape')
        formcomponent.director = director
        # build the form 
        form = document.form(name='', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'sampleInput', 
            sentry = director.sentry,
            routine = 'onShapeSelect',
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
        return page  
    
    def onShapeSelect(self, director):
        selected = self.processFormInputs(director)
        method = getattr(self, selected )
        return method( director )
        
    def inputPlate(self, director):
        try:
            page = director.retrieveSecurePage('generic')
        except AuthenticationError, err:
            return err.page
#        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        main = page._body._content._main
        # populate the main column
        document = main.document(title='Shape input')
        document.description = ''
        document.byline = '<a href="http://danse.us">DANSE</a>'        
        
        formcomponent = self.retrieveFormToShow( 'inputPlate')
        formcomponent.director = director
        # build the form 
        form = document.form(name='', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'sample', 
            sentry = director.sentry,
            routine = 'default',
            label = '',
            id=self.inventory.id,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        submit = form.control(name='submit',type="submit", value="submit")
        self.processFormInputs(director)
        return page
    
    def inputCylinder(self, director):
        try:
            page = director.retrieveSecurePage('generic')
        except AuthenticationError, err:
            return err.page
#        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        main = page._body._content._main
        # populate the main column
        document = main.document(title='Shape input')
        document.description = ''
        document.byline = '<a href="http://danse.us">DANSE</a>'        
        
        formcomponent = self.retrieveFormToShow( 'inputCylinder')
        formcomponent.director = director
        # build the form 
        form = document.form(name='', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'sample', 
            sentry = director.sentry,
            routine = 'default',
            label = '',
            id=self.inventory.id,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        submit = form.control(name='submit',type="submit", value="submit")
        self.processFormInputs(director)
        return page


    def __init__(self, name=None):
        if name is None:
            name = "sampleInput"
        super(SampleInput, self).__init__(name)
        return

    def _createSample(self, director, matter=None):

        type = self.inventory.type
        Computation = director.clerk._getTable(type)
        
        computation = director.clerk.newDbObject(Computation)
        self.inventory.id = id = computation.id
        computation.matter = matter
        director.clerk.updateRecord(computation)
        return computation






# version
__id__ = "$Id$"

# End of file 
