#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Actor import Actor, action_link, action, actionRequireAuthentication, AuthenticationError

from FormActor import FormActor as base

class ScatteringKernelInput(base):

#    @staticmethod
    def default(self, director):
        try:
            page, document = self._head( director )
        except AuthenticationError, err:
            return err.page
        formcomponent = self.retrieveFormToShow( 'selectkernel')
        formcomponent.director = director
        # build the SKChoice form
        SKChoice = document.form(name='scatteringKernelInput', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'scatteringKernelInput', 
            sentry = director.sentry,
            routine = 'onSelect',
            label = '',
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, SKChoice )
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( SKChoice )
        submit = SKChoice.control(name='submit',type="submit", value="next")
        return page 
    
    def onSelect(self, director):
        selected = self.processFormInputs(director)
        method = getattr(self, selected )
        return method( director )

    def gulp(self, director):
        try:
            page = director.retrieveSecurePage( 'gulp' )
        except AuthenticationError, err:
            return err.page
        main = page._body._content._main
        document = main.document(title="")
        document.byline = '<a href="http://danse.us">DANSE</a>'
        
        formcomponent = self.retrieveFormToShow( 'gulp')
        formcomponent.director = director
        # build the SKChoice form
        form = document.form(name='scatteringKernelInput', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'job', 
            sentry = director.sentry,
            routine = 'edit',
            label = '',
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        submit = form.control(name='submit',type="submit", value="next")
        return page 
    
    def abInitioHarmonic(self, director):
        try:
            page = director.retrieveSecurePage( 'abInitioHarmonic' )
        except AuthenticationError, err:
            return err.page
        main = page._body._content._main
        document = main.document(title="")
        document.byline = '<a href="http://danse.us">DANSE</a>'
        
        formcomponent = self.retrieveFormToShow( 'abInitioHarmonic')
        formcomponent.director = director
        # build the SKChoice form
        form = document.form(name='scatteringKernelInput', action=director.cgihome)
        # specify action
        action = actionRequireAuthentication(          
            actor = 'job', 
            sentry = director.sentry,
            routine = 'edit',
            label = '',
            arguments = {'form-received': formcomponent.name },
            )
        from vnf.weaver import action_formfields
        action_formfields( action, form )
        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )
        submit = form.control(name='scatteringKernelInput.submit',type="submit", value="next")
        return page 
        
    def __init__(self, name=None):
        if name is None:
            name = "scatteringKernelInput"
        super(ScatteringKernelInput, self).__init__(name)
    
    def _head(self, director):
        page = director.retrieveSecurePage( 'scatteringKernelInput' )
        main = page._body._content._main
        # the record we are working on
        id = None # eventually get the id from idd
        document = main.document(title='Energetics / Dynamics Selection' )
        document.byline = '<a href="http://danse.us">DANSE</a>'
        return page, document


# version
__id__ = "$Id$"

# End of file 
