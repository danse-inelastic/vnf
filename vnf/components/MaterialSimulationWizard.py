#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2008  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Actor import actionRequireAuthentication, action_link, AuthenticationError
from FormActor import FormActor as base, InputProcessingError


class MaterialSimulationWizard(base):
    
    
    class Inventory(base.Inventory):
        
        import pyre.inventory
        
        id = pyre.inventory.str("id", default='')
        id.meta['tip'] = "the unique identifier of the experiment"

        matterid = pyre.inventory.str('matterid')
        mattertype = pyre.inventory.str('mattertype')

        pass # end of Inventory


    def default(self, director):
        return self.start(director)

    def start(self, director):
        return self.selectmaterial(director)
    

    def selectmaterial(self, director):
        try:
            page = director.retrieveSecurePage( 'materialsimulationwizard' )
        except AuthenticationError, err:
            return err.page

        main = page._body._content._main

        # populate the main column
        document = main.document(title='Material Simulation/Modeling Wizard: select material')
        document.description = ''
        document.byline = 'byline?'

        formcomponent = self.retrieveFormToShow(
            'selectmaterial' )
        formcomponent.director = director
        
        # create form
        form = document.form(
            name='selectmaterial',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'materialsimulationwizard', sentry = director.sentry,
            label = '', routine = 'verify_material_selection',
            id = self.inventory.id,
            arguments = {'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        # run button
        submit = form.control(name="actor.form-received.submit", type="submit", value="Continue")

        return page
    

    def verify_material_selection(self, director):
        try:
            page = director.retrieveSecurePage( 'materialsimulationwizard' )
        except AuthenticationError, err:
            return err.page

        mattertype,matterid = self.processFormInputs(director)
        self.inventory.matterid = matterid
        self.inventory.mattertype = mattertype
        
        return self.selectsimulationtype(director)


    def selectsimulationtype(self, director):
        try:
            page = director.retrieveSecurePage( 'materialsimulationwizard' )
        except AuthenticationError, err:
            return err.page

        main = page._body._content._main

        # populate the main column
        document = main.document(title='Material Simulation/Modeling Wizard: start')
        document.description = ''
        document.byline = 'byline?'

        formcomponent = self.retrieveFormToShow(
            'selectmaterialsimulationtype' )
        formcomponent.director = director
        
        # create form
        form = document.form(
            name='selectmaterialsimulationtype',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'materialsimulationwizard', sentry = director.sentry,
            label = '', routine = 'verify_materialsimulationtype_selection',
            id = self.inventory.id,
            matterid = self.inventory.matterid,
            mattertype = self.inventory.mattertype,
            arguments = {'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        # run button
        submit = form.control(name="actor.form-received.submit", type="submit", value="Continue")

        return page


    def verify_materialsimulationtype_selection(self, director):
        try:
            page = director.retrieveSecurePage( 'materialsimulationwizard' )
        except AuthenticationError, err:
            return err.page

        type = self.processFormInputs(director)
        type = type.replace(' ', '_').lower()
        routine = 'configure_simulation'

        mattertype = self.inventory.mattertype
        matterid = self.inventory.matterid
        matter = director.clerk.getRecordByID(mattertype, matterid)
        
        return self.redirect(director, type, routine, matter = matter)

    def selectSimulationEngine(self, director):
        try:
            page = director.retrieveSecurePage( 'materialsimulationwizard' )
        except AuthenticationError, err:
            return err.page
#        experiment = director.clerk.getNeutronExperiment(self.inventory.id)
        main = page._body._content._main
        # populate the main column
        document = main.document(
            title='Kernel model selection')
        document.description = ''
        document.byline = '<a href="http://danse.us">DANSE</a>'        
        
        formcomponent = self.retrieveFormToShow( 'selectSimulationEngine')
        formcomponent.director = director
        # build the form 
        form = document.form(name='', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'materialsimulationwizard', 
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
        return page    
    
    def onSelect(self, director):
        selected = self.processFormInputs(director)
        method = getattr(self, selected )
        return method( director )

    def gulp(self, director):
        try:
            page = director.retrieveSecurePage( 'materialsimulationwizard' )
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
            actor = 'materialsimulationwizard', 
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
        return page 
   
    def localOrbitalHarmonic(self, director):
        try:
            page = director.retrieveSecurePage( 'materialsimulationwizard' )
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
            actor = 'materialsimulationwizard', 
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
        return page 
    
    def planeWaveHarmonic(self, director):
        try:
            page = director.retrieveSecurePage( 'materialsimulationwizard' )
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
            actor = 'materialsimulationwizard', 
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
        return page 
    
    def kernel_generator(self, director):
        try:
            page = director.retrieveSecurePage( 'materialsimulationwizard' )
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
            actor = 'materialsimulationwizard', 
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
        return page     


    def configure_simulation(self, director):
        raise NotImplementedError


    def __init__(self, name=None):
        if name is None:
            name = "materialsimulationwizard"
        super(MaterialSimulationWizard, self).__init__(name)
        return


    pass # end of MaterialSimulationWizard


from misc import new_id, empty_id, nullpointer

# version
__id__ = "$Id$"

# End of file 
