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


from Actor import Actor, action_link, action, actionRequireAuthentication, AuthenticationError

from FormActor import FormActor as base


class Instrument(base):


    class Inventory(base.Inventory):

        import time
        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier of the instrument"

        import vnf.inventory
        geometer = vnf.inventory.geometer( 'geometer' )

        editee = pyre.inventory.str('editee', default = 'instrument,#id#')
        editee.meta['tip'] = 'The sub element to edit for edit routine'

        pass # end of Inventory



    def default(self, director):
        return self.listall( director )


    def listall(self, director):
        try:
            page = director.retrieveSecurePage( 'instrument' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        # populate the main column
        document = main.document(title='List of instruments')
        document.description = ''
        document.byline = 'byline?'

        # retrieve id:record dictionary from db
        clerk = director.clerk
        instruments = clerk.indexInstruments()
        
        listinstruments( instruments.values(), document, director )
        
        return page


    def edit(self, director):
        try:
            page = director.retrieveSecurePage( 'sampleassembly' )
        except AuthenticationError, err:
            return err.page

        elementtype, elementid = self.inventory.editee.split(',')
        if elementtype == 'instrument': elementid = self.inventory.id
        
        formcomponent = self.retrieveFormToShow( elementtype )
        formcomponent.inventory.id = elementid
        formcomponent.director = director

        # start document
        main = page._body._content._main
        document = self._document( main, director )
        self._tree( document, director )
        
        # create form
        form = document.form(
            name='instrument',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'instrument', sentry = director.sentry,
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
            'To edit this instrument, please click a link in the tree.',
            ]
        return page


    def __init__(self, name=None):
        if name is None:
            name = "instrument"
        super(Instrument, self).__init__(name)
        return


    def _document(self, main, director):
        # the record we are working on
        id = self.inventory.id
        instrument = self._getinstrument( director )

        # populate the main column
        document = main.document(title='Instrument: %s' % instrument.short_description )
        document.description = (
            'Instrument is a collection of neutron components. For example, '\
            'it can consist of a neutron source, a sample, and a detector system.\n'\
            )
        document.byline = '<a href="http://danse.us">DANSE</a>'
        return document


    def _tree(self, document, director):
        instrument = self._getinstrument( director )
        from TreeViewCreator import create as create_treeview
        treeview = create_treeview(
            director.clerk.getHierarchy(instrument),
            'instrument',
            director)
        document.contents.append(  treeview )
        return


    def _getinstrument(self, director):
        id = self.inventory.id
        clerk = director.clerk
        return clerk.getInstrument( id )


    def _configure(self):
        base._configure(self)
        self.id = self.inventory.id
        form_received = self.form_received = self.inventory.form_received
        if form_received.name == 'instrument':
            form_received.inventory.id = self.id
            pass
        return


    pass # end of Instrument



from wording import plural, present_be

def listinstruments( instruments, document, director ):
    p = document.paragraph()

    n = len(instruments)

    p.text = [ 'There %s %s instrument%s: ' %
               (present_be(n), n, plural(n))
                ]

    from inventorylist import list
    list( instruments, document, 'instrument', director )
    return



def build_run( instrument ):
    from InstrumentSimulationRunBuilder import Builder
    return Builder().render(instrument)


# version
__id__ = "$Id$"

# End of file 
