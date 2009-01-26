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
        
        polycrystalId = pyre.inventory.str("polycrystalId", default=None)
        polycrystalId.meta['tip'] = "the unique identifier for a given material"
        
        singlecrystalId = pyre.inventory.str("singlecrystalId", default=None)
        singlecrystalId.meta['tip'] = "the unique identifier for a given material"
        
        disorderedId = pyre.inventory.str("disorderedId", default=None)
        disorderedId.meta['tip'] = "the unique identifier for a given material"
        
        sampleId = pyre.inventory.str("sampleId", default=None)
        sampleId.meta['tip'] = "the unique identifier for a given sample shape"
        
        page = pyre.inventory.str('page', default='empty')

    def default(self, director):
        return self.selectMaterialType(director)
    
    def selectMaterialType(self, director):
        try:
            page = director.retrieveSecurePage( 'generic' )
        except AuthenticationError, err:
            return err.page
#        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        main = page._body._content._main
        # populate the main column
        document = main.document(title='Material type selection')
        document.description = ''
        document.byline = '<a href="http://danse.us">DANSE</a>'        
        
        formcomponent = self.retrieveFormToShow( 'selectmaterialtype')
        formcomponent.director = director
        # build the form 
        form = document.form(name='', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'sampleInput', 
            sentry = director.sentry,
            routine = 'redirectMaterialInput',
            label = '',
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        submit = form.control(name='submit',type="submit", value="next")
        #self.processFormInputs(director)
        return page 
    
    def redirectMaterialInput(self, director):
        selected = self.processFormInputs(director)
        method = getattr(self, selected )
        return method( director )
        
    def polycrystal(self, director):
        try:
            page = director.retrievePage( 'generic' )
        except AuthenticationError, err:
            return err.page
        
#        polycrystalTableClass = director.clerk._getTable('polycrystal')
#        polycrystalDbObject = director.clerk.newDbObject(polycrystalTableClass)
#        polycrystalId = self.inventory.polycrystalId = polycrystalDbObject.id
        
#        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        main = page._body._content._main
        # populate the main column
        document = main.document(title='Material input')
        document.description = ''
        document.byline = '<a href="http://danse.us">DANSE</a>'        
        
        formcomponent = self.retrieveFormToShow('polycrystal')
        formcomponent.director = director
        # build the form 
        form = document.form(name = '', action = director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'sampleInput', 
            sentry = director.sentry,
            routine = 'storeAndVerifyMatterInput',
            label = '',
            #id = polycrystalId,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form , #id = polycrystalId, 
                              materialType = 'polycrystal', showimportwidget=True)
        submit = form.control(name='submit',type="submit", value="next")
        return page  
    
    def singlecrystal(self, director):
        try:
            page = director.retrievePage( 'generic' )
        except AuthenticationError, err:
            return err.page
        
#        polycrystalTableClass = director.clerk._getTable('polycrystal')
#        polycrystalDbObject = director.clerk.newDbObject(polycrystalTableClass)
#        polycrystalId = self.inventory.polycrystalId = polycrystalDbObject.id
        
#        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        main = page._body._content._main
        # populate the main column
        document = main.document(title='Material input')
        document.description = ''
        document.byline = '<a href="http://danse.us">DANSE</a>'                

        formcomponent = self.retrieveFormToShow('singlecrystal')
        formcomponent.director = director
        # build the form 
        form = document.form(name = '', action = director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'sampleInput', 
            sentry = director.sentry,
            routine = 'storeAndVerifyMatterInput',
            label = '',
            #id = polycrystalId,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form , #id = polycrystalId, 
                              materialType = 'singlecrystal', showimportwidget=True)
        submit = form.control(name='submit',type="submit", value="next")
        return page  
    
    def disordered(self, director):
        try:
            page = director.retrievePage( 'generic' )
        except AuthenticationError, err:
            return err.page
        
#        polycrystalTableClass = director.clerk._getTable('polycrystal')
#        polycrystalDbObject = director.clerk.newDbObject(polycrystalTableClass)
#        polycrystalId = self.inventory.polycrystalId = polycrystalDbObject.id
        
#        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        main = page._body._content._main
        # populate the main column
        document = main.document(title='Material input')
        document.description = ''
        document.byline = '<a href="http://danse.us">DANSE</a>'        
        
        formcomponent = self.retrieveFormToShow('disordered')
        formcomponent.director = director
        # build the form 
        form = document.form(name = '', action = director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'sampleInput', 
            sentry = director.sentry,
            routine = 'storeAndVerifyMatterInput',
            label = '',
            #id = polycrystalId,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form , #id = polycrystalId, 
                    materialType = 'disordered')
        submit = form.control(name='submit',type="submit", value="next")
        return page 
    
    def storeAndVerifyMatterInput(self, director):
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
            #id=self.inventory.id,
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
        
        formcomponent = self.retrieveFormToShow( 'inputBlock')
        formcomponent.director = director
        # build the form 
        form = document.form(name='', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'sampleInput', 
            sentry = director.sentry,
            routine = 'storeAndVerifyShapeInput',
            label = '',
            #id=self.inventory.id,
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
            actor = 'sampleInput', 
            sentry = director.sentry,
            routine = 'storeAndVerifyShapeInput',
            label = '',
            #id=self.inventory.id,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        submit = form.control(name='submit',type="submit", value="submit")
        self.processFormInputs(director)
        return page
    
    def storeAndVerifyShapeInput(self, director):
        self.processFormInputs(director) 
        actor = 'sample'
        routine = 'default'
        return director.redirect(actor, routine)

    def __init__(self, name=None):
        if name is None:
            name = "sampleInput"
        super(SampleInput, self).__init__(name)
        return

    







# version
__id__ = "$Id$"

# End of file 
