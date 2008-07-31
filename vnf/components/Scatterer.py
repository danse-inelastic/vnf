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


from Actor import action_link, actionRequireAuthentication, AuthenticationError

from FormActor import FormActor as base


class Scatterer(base):


    class Inventory(base.Inventory):

        import time
        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier for a given search"
        
        pass # end of Inventory



    def default(self, director):
        return self.listall( director )


    def listall(self, director):
        try:
            page = director.retrieveSecurePage( 'scatterer' )
        except AuthenticationError, error:
            return error.page
        
        main = page._body._content._main
        
        # populate the main column
        document = main.document(title='List of scatterers')
        document.description = ''
        document.byline = 'byline?'

        # retrieve id:record dictionary from db
        clerk = director.clerk
        scatterers = clerk.indexScatterers( where = 'template="True"' )
        
        listscatterers( scatterers.values(), document, director )
        
        return page


    def selectshapetype(self, director):
        try:
            page = director.retrieveSecurePage( 'scatterer' )
        except AuthenticationError, error:
            return error.page

        main = page._body._content._main

        # populate the main column
        document = main.document(title='Scatterer shape')
        document.description = ''
        document.byline = 'byline?'

        self.processFormInputs( director )

        id = self.inventory.id
        realscatterer = record = director.clerk.getRealScatterer( id )

        # new abstract shape record
        from Shape import new_shape
        shape = new_shape( director )

        # refer to the new shape record
        realscatterer.shape_id = shape.id
        director.clerk.updateRecord( realscatterer )

        #
        # create form
        formcomponent = self.retrieveFormToShow( 'selectshapetype' )
        formcomponent.inventory.id = shape.id
        formcomponent.director = director
        
        form = document.form(
            name='selectshapetype',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'scatterer', sentry = director.sentry,
            label = '',
            routine = 'editshape',
            arguments = { 'id': self.inventory.id,
                          'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        # ok button
        submit = form.control(name="submit", type="submit", value="OK")
        
        return page


    def editshape(self, director):
        try:
            page = director.retrieveSecurePage( 'scatterer' )
        except AuthenticationError, error:
            return error.page

        main = page._body._content._main

        # populate the main column
        document = main.document(title='Scatterer shape')
        document.description = ''
        document.byline = 'byline?'

        self.processFormInputs( director )

        realscatterer = director.clerk.getRealScatterer( self.inventory.id )
        realshape = director.clerk.getRealShape( realscatterer.shape_id )

        # create form
        formcomponent = self.retrieveFormToShow(
            realshape.__class__.__name__.lower() )
        formcomponent.inventory.id = realshape.id
        formcomponent.director = director
        
        form = document.form(
            name='editshape',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'scatterer', sentry = director.sentry,
            label = '',
            routine = 'edit_%s_start' % realscatterer.__class__.__name__.lower(),
            arguments = { 'id': self.inventory.id,
                          'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        # ok button
        submit = form.control(name="submit", type="submit", value="OK")
        
        return page


    def edit_crystal(self, submit_routine, director):
        try:
            page = director.retrieveSecurePage( 'scatterer' )
        except AuthenticationError, error:
            return error.page

        main = page._body._content._main

        # populate the main column
        document = main.document(title='Crystal')
        document.description = ''
        document.byline = 'byline?'

        self.processFormInputs( director )

        id = self.inventory.id
        realscatterer = director.clerk.getRealScatterer( id )
        crystal_id = realscatterer.crystal_id

        # create form
        formcomponent = self.retrieveFormToShow( 'crystal' )
        formcomponent.inventory.id = crystal_id
        formcomponent.director = director
        
        form = document.form(
            name='editcrystal',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'scatterer', sentry = director.sentry,
            label = '',
            routine = submit_routine,
            arguments = { 'id': self.inventory.id,
                          'form-received': formcomponent.name,
                          'form-received.id': crystal_id,
                          } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        # ok button
        submit = form.control(name="submit", type="submit", value="OK")
        
        return page


    def edit_polyxtalscatterer_start(self, director):
        return self.edit_crystal( 'edit_polyxtalscatterer_end', director )


    def edit_polyxtalscatterer_end(self, director):
        try:
            page = director.retrieveSecurePage( 'scatterer' )
        except AuthenticationError, error:
            return error.page

        main = page._body._content._main

        # populate the main column
        document = main.document(title='Polycrystal Scatterer')
        document.description = ''
        document.byline = 'byline?'

        self.processFormInputs( director )

        id = self.inventory.id
        polyxtalscatterer = director.clerk.getRealScatterer( id )

        # create form
        formcomponent = self.retrieveFormToShow( 'polyxtalscatterer' )
        formcomponent.inventory.id = polyxtalscatterer.id
        formcomponent.director = director
        
        form = document.form(
            name='editpolyxtalscatterer',
            legend= formcomponent.legend(),
            action=director.cgihome)

        sa_id = director.clerk.findParentSampleAssembly( id ).id
        
        # specify action
        action = actionRequireAuthentication(
            actor = 'sampleassembly', sentry = director.sentry,
            label = '',
            routine = 'set',
            arguments = { 'id': sa_id,
                          'form-received': formcomponent.name,
                          'form-received.id': polyxtalscatterer.id,
                          } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        # ok button
        submit = form.control(name="submit", type="submit", value="OK")
        
        return page


    def __init__(self, name=None):
        if name is None:
            name = "scatterer"
        super(Scatterer, self).__init__(name)
        return


    def _getscatterer(self, id, director):
        clerk = director.clerk
        return clerk.getScatterer( id )


    pass # end of Scatterer


from wording import plural, present_be

def listscatterers( scatterers, document, director ):
    p = document.paragraph()

    n = len(scatterers)
    p.text = [ 'There %s %s scatterer%s: ' %
               (present_be(n), n, plural(n))
                ]

    from inventorylist import list
    list( scatterers, document, 'scatterer', director )
    
    return



def noscatterer( document, director ):
    p = document.paragraph()

    link = action_link(
        actionRequireAuthentication(
        'scatterer', director.sentry,
        label = 'add', routine = 'new',
        ),  director.cgihome
        )
    
    p.text = [
        "There is no scatterer. ",
        'Please %s a scatter.' % (
        director.cgihome, link)
        ]
    return



def new_id( director ):
    #new token
    token = director.idd.token()
    uniquename = '%s-%s-%s' % (token.locator, token.tid, token.date)
    return uniquename


def new_scatterer( director ):
    from vnf.dom.Scatterer import Scatterer
    record = Scatterer()

    id = new_id( director )
    record.id = id

    import time
    record.date = time.ctime()

    director.clerk.newRecord( record )
    
    return record


from misc import new_id

# version
__id__ = "$Id$"

# End of file 
