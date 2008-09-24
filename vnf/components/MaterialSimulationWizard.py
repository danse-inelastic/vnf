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

        type = pyre.inventory.str('type')

        pass # end of Inventory


    def start(self, director):
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
        routine = 'configure%s'%type
        return self.redirect(director, type, routine)


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
