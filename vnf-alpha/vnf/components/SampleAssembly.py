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


deletables = [
    'polyxtalscatterer',
    #'scatteringkernel',
    ]

from Actor import action_link, action, actionRequireAuthentication, AuthenticationError

from FormActor import FormActor as base

class SampleAssembly(base):

    class Inventory(base.Inventory):

        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier of the sample assembly"

        editee = pyre.inventory.str('editee', default = 'sampleassembly,#id#')
        editee.meta['tip'] = 'The sub element to edit for edit routine'



    def default(self, director):
        return self.listall(director)
    

    def new(self, director):
        try:
            page = director.retrieveSecurePage( 'sampleassembly' )
        except AuthenticationError, err:
            return err.page

        sampleassembly = new_sampleassembly( director )
        self.inventory.id = sampleassembly.id
        return self.edit( director )
    

    def listall(self, director):
        try:
            page = director.retrieveSecurePage( 'sampleassembly' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        # populate the main column
        document = main.document(title='List of sample assemblies')
        document.description = ''
        document.byline = 'byline?'

        p = document.paragraph()
        link = action_link(
            actionRequireAuthentication(
                'sampleassembly',
                director.sentry,
                label = 'link',
                routine = 'new',
                ),  director.cgihome
            )
        p.text = [
            'To create a new sample assembly, please use this %s' % link
            ]

        p = document.paragraph()
        p = document.paragraph()

        # retrieve id:record dictionary from db
        clerk = director.clerk
        sampleassemblies = clerk.indexSampleAssemblies()
        
        listsampleassemblies( sampleassemblies.values(), document, director )
        
        return page


    def edit(self, director):
        try:
            page = director.retrieveSecurePage( 'sampleassembly' )
        except AuthenticationError, err:
            return err.page

        #subcomponent to edit
        elementtype, elementid = self.inventory.editee.split(',')
        if elementtype == 'sampleassembly': elementid = self.inventory.id

        handler = 'edit_%s' % elementtype
        try:
            handler = getattr(self, handler)
        except AttributeError:
            handler = None
            pass
        if handler: return handler( elementid, director ) 
        
        formcomponent = self.retrieveFormToShow( elementtype )
        formcomponent.inventory.id = elementid
        formcomponent.director = director

        # start document
        main = page._body._content._main
        document = self._document( main, director )
        self._tree( document, director )
        
        # start form
        form = document.form(
            name='sampleassembly',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # add a line to allow delete of object
        if elementtype.lower() in deletables:
            p = form.paragraph()
            link = action_link(
                actionRequireAuthentication(
                    'sampleassembly',
                    director.sentry,
                    label = 'Delete this %s' % elementtype.lower(),
                    routine = 'delete_subelement',
                    id = self.inventory.id,
                    editee = self.inventory.editee,
                    ),  director.cgihome
                )
            p.text = [ link ]
            pass

        # specify action
        action = actionRequireAuthentication(
            actor = 'sampleassembly', sentry = director.sentry,
            label = '', routine = 'set',
            arguments = { 'id': self.inventory.id,
                          'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        # ok button
        submit = form.control(name="submit", type="submit", value="OK")
        
        return page


    def delete(self, director):
        try:
            page = director.retrieveSecurePage( 'sampleassembly' )
        except AuthenticationError, error:
            return error.page

        record = director.clerk.getSampleAssembly( self.inventory.id )
        name = record.short_description
        
        director.clerk.deleteRecord( record )

        return self.listall(director)
        

    def delete_subelement(self, director):
        try:
            page = director.retrieveSecurePage( 'sampleassembly' )
        except AuthenticationError, error:
            return error.page

        main = page._body._content._main
        document = self._document( main, director )

        elementtype, elementid = self.inventory.editee.split(',')
        
        assert elementtype in deletables, '%r is not deletable' % elementtype

        method = 'delete_%s' % elementtype.lower()
        method = getattr( self, method )
        method( elementid, director )

        self._tree( document, director )

        return page


    def delete_polyxtalscatterer(self, id, director):
        clerk = director.clerk
        record = clerk.getAbstractScatterer( 'PolyXtalScatterer', id )
        return self.delete_scatterer( record.id, director )


    def delete_scatterer(self, id, director ):
        director.clerk.deleteScattererFromSampleAssembly(
            id, self.inventory.id )
        return


    def set(self, director):
        try:
            page = director.retrieveSecurePage( 'sampleassembly' )
        except AuthenticationError, error:
            return error.page

        self.processFormInputs( director )
        
        main = page._body._content._main
        document = self._document( main, director )

        self._tree( document, director )

        p = document.paragraph()
        p.text = [
            'To edit this sample assembly, please click a link in the tree.',
            ]
        return page


    def addnewscatterer(self, director ):
        try:
            page = director.retrieveSecurePage( 'sampleassembly' )
        except AuthenticationError, error:
            return error.page

        # create new abstract scatterer record
        from Scatterer import new_scatterer
        scatterer = new_scatterer(director)

        # add new scatterer to sample assembly
        reference = new_reference(
            self.inventory.id, scatterer.id, director )

        return self.edit_scatterer( scatterer.id, director )


    def edit_scatterer(self, scatterer_id, director):
        try:
            page = director.retrieveSecurePage( 'sampleassembly' )
        except AuthenticationError, error:
            return error.page

        scatterer = director.clerk.getScatterer( scatterer_id )

        main = page._body._content._main
        document = self._document( main, director )
        self._tree( document, director )        

        # create form to set scatterer type
        formcomponent = self.retrieveFormToShow( 'selectscatterertype' )
        formcomponent.inventory.id = scatterer.id
        formcomponent.director = director
        
        # create form
        form = document.form(
            name='selectscatterertype',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'scatterer', sentry = director.sentry,
            label = '', routine = 'selectshapetype',
            arguments = { 'id': scatterer.id,
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
            name = "sampleassembly"
        super(SampleAssembly, self).__init__(name)
        return


    def _document(self, main, director):
        # the record we are working on
        id = self.inventory.id
        sampleassembly = self._getsampleassembly( director )

        # populate the main column
        document = main.document(title='Sample Assembly: %s' % sampleassembly.short_description )
        document.description = (
            'Sample assembly is a collection of neutron scatterers. For example, '\
            'it can consist of a main sample, a sample container, and a furnace.\n'\
            )
        document.byline = '<a href="http://danse.us">DANSE</a>'
        return document


    def _tree(self, document, director):
        sampleassembly = self._getsampleassembly( director )
        treeview = create_treeview(
            director.clerk.getHierarchy(sampleassembly),
            director)
        document.contents.append(  treeview )
        return


    def _getsampleassembly(self, director):
        id = self.inventory.id
        clerk = director.clerk
        return clerk.getSampleAssembly( id )


    def _configure(self):
        base._configure(self)
        self.id = self.inventory.id
        form_received = self.form_received = self.inventory.form_received
        if form_received.name == 'sampleassembly':
            form_received.inventory.id = self.id
            pass
        return


    pass # end of SampleAssembly



from wording import plural, present_be

def listsampleassemblies( sampleassemblies, document, director ):
    p = document.paragraph()

    n = len(sampleassemblies)

    p.text = [ 'There %s %s existing sampleassembl%s: ' %
               (present_be(n), n, plural(n, 'y'))
                ]

    from inventorylist import list
    list( sampleassemblies, document, 'sampleassembly', director,
          routines = ( 'edit', 'delete' )
          )
    return



def noscatterer( document, director ):
    p = document.paragraph()

    link = action_link(
        actionRequireAuthentication(
        'scatterer',
        director.sentry,
        label = 'add',
        routine = 'new',
        ),  director.cgihome
        )
    
    p.text = [
        "There is no scatterer in this sample assembly. ",
        'Please %s a scatter.' % (
        director.cgihome, link)
        ]
    return



    

def create_treeview( sampleassembly, director ):
    '''given the db hierarchy of sampleassembly, render a teeview
    '''
    from TreeViewCreator import create
    return create(sampleassembly, 'sampleassembly', director )



from misc import new_id

def new_reference( sampleassembly_id, scatterer_id, director ):
    from vnf.dom.SampleAssembly import SampleAssembly
    record = SampleAssembly.Scatterers()

    id = new_id( director )
    record.id = id

    record.localkey = sampleassembly_id
    record.remotekey = scatterer_id

    director.clerk.newRecord( record )
    
    return record



def new_sampleassembly( director ):
    from vnf.dom.SampleAssembly import SampleAssembly
    record = SampleAssembly()

    id = new_id( director )
    record.id = id

    record.constructed = False
    record.short_description = ''
    record.creator = director.sentry.username

    import time
    record.date = time.ctime()

    director.clerk.newRecord( record )
    
    return record


            

# version
__id__ = "$Id$"

# End of file 
