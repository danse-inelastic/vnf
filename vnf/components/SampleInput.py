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

        sampleId = pyre.inventory.str("sampleId", default='')
        sampleId.meta['tip'] = "the unique identifier for a given sample"
        
#        polycrystalId = pyre.inventory.str("polycrystalId", default=None)
#        polycrystalId.meta['tip'] = "the unique identifier for a given material"
#        
#        singlecrystalId = pyre.inventory.str("singlecrystalId", default=None)
#        singlecrystalId.meta['tip'] = "the unique identifier for a given material"
#        
#        disorderedId = pyre.inventory.str("disorderedId", default=None)
#        disorderedId.meta['tip'] = "the unique identifier for a given material"
        
        page = pyre.inventory.str('page', default='empty')

    def default(self, director):
        return self.sampleDescription(director)
    
    def sampleDescription(self, director):
        try:
            page = director.retrieveSecurePage( 'generic' )
        except AuthenticationError, err:
            return err.page
        
        # put this part after clicking the previous link in Sample page instead
        # of here
#        if self.inventory.sampleId == '':
#            # create a new sample
#            from vnf.dom.Sample import Sample
#            sample = director.clerk.newObject( Sample )
#            self.inventory.sampleId = sample.id
        
        main = page._body._content._main
        # populate the main column
        document = main.document(title='Material type selection')
        document.description = ''
        document.byline = '<a href="http://danse.us">DANSE</a>'        
        
        formcomponent = self.retrieveFormToShow( 'sampleDescription')
        formcomponent.director = director
        # build the form 
        form = document.form(name='', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'sampleInput', 
            sentry = director.sentry,
            routine = 'storeSampleDescription',
            label = '',
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form, id = self.inventory.sampleId)
        submit = form.control(name='submit',type="submit", value="next")
        return page         
    
    def storeSampleDescription(self, director):
        short_description = self.processFormInputs( director )
        try: # first try to get a record with the inventory id from the db
            record = director.clerk.getRecordByID('sample', self.inventory.sampleId)
        except: # if can't find, create a new one
            tableClass = director.clerk._getTable('sample')
            record = director.clerk.newDbObject(tableClass)
            self.inventory.sampleId = record.id

        record.short_description = short_description

        # and update db
        director.clerk.updateRecord( record )
        return self.selectMaterialType( director )
    
    def selectMaterialType(self, director):
        try:
            page = director.retrieveSecurePage( 'generic' )
        except AuthenticationError, err:
            return err.page
        
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
            sampleId = self.inventory.sampleId,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        submit = form.control(name='submit',type="submit", value="next")
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
            sampleId = self.inventory.sampleId,
            #id = polycrystalId,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form , showimportwidget=True)
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
            sampleId = self.inventory.sampleId,
            #id = polycrystalId,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form , showimportwidget=True)
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
            sampleId = self.inventory.sampleId,
            #id = polycrystalId,
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        submit = form.control(name='submit',type="submit", value="next")
        return page 
    
    def storeAndVerifyMatterInput(self, director):
        #store matter
        matter =self.processFormInputs(director)
        # attach matter to sample and store 
        sample = director.clerk.getRecordByID('samples', self.inventory.sampleId)
        sample.matter = matter
        director.clerk.updateRecord(sample)
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
            sampleId = self.inventory.sampleId,
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
        
    def inputBlock(self, director):
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
            sampleId = self.inventory.sampleId,
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
            sampleId = self.inventory.sampleId,
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
        # store shape
        shape = self.processFormInputs(director) 
        # attach shape to sample and store 
        sample = director.clerk.getRecordByID('samples', self.inventory.sampleId)
        sample.shape = shape
        director.clerk.updateRecord(sample)
        
        actor = 'sample'
        routine = 'default'
        return director.redirect(actor, routine)

#    def _retrievePage(self, director):
#        page = 'sample'
#
#        sampleId = self.inventory.sampleId
#        if sampleId:
#            sample = director.clerk.getNeutronExperiment(id)
#            if sample.matter:
#                instrument = director.clerk.dereference(iref)
#                if _instrument_without_sample(instrument, director.clerk.db):
#                    page = 'neutronexperimentwizard-nosample'
#        return director.retrieveSecurePage(page)

    def __init__(self, name=None):
        if name is None:
            name = "sampleInput"
        super(SampleInput, self).__init__(name)
        return

    







# version
__id__ = "$Id$"

# End of file 
