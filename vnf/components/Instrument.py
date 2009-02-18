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
import os
import vnf.content


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


    def show(self, director):
        '''show info of an instrument'''
        try:
            page = director.retrieveSecurePage( 'instrument' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        instrument = self._getinstrument( director )

        # populate the main column
        title = 'Instrument #%s: %s' % (instrument.id, instrument.short_description)
        document = main.document(title=title)
        document.byline = 'byline?'

        long_description = instrument.long_description
        for paragraph in long_description.split( '\n' ):
            p = document.paragraph()
            p.text = [ paragraph ]
            continue

        # put up a graph
        #schematic = os.path.join( self._imageStore( instrument ), 'schematic.png' )
        schematic = director.dds.path(instrument, 'schematic.png')
        if os.path.exists(director.dds.abspath(instrument, 'schematic.png')):
            schematic = vnf.content.image( schematic )
            document.contents.append( schematic )

        # link for 3d view
        p = document.paragraph()
        view3d = actionRequireAuthentication(
            label = '3d view',
            sentry = director.sentry,
            id = self.inventory.id,
            actor = 'instrument',
            routine = 'view3d',
            )
        link = action_link(view3d, director.cgihome)
        p.text = [
            '%s' % link,
            ]

        # empty line
        p = document.paragraph()

        if not self._isAccessible(instrument, director):

            # instrument not accessible
            p = document.paragraph(cls='error')
            p.text = [
                'You are not authorized to do experiments wiith this instrument',
                ]
        
        else:

            # experiment planning link
            p = document.paragraph()
            experimentplanning = actionRequireAuthentication(
                actor = '%sexperimentwizard' % instrument.id,
                sentry = director.sentry,
                label = 'planning',
                routine = 'start',
                )
            p.text = [
                'Start %s for an experiment on %s' % (
                action_link( experimentplanning, director.cgihome ), instrument.short_description ),
                ]

            # edit link
            if instrument.creator == director.sentry.username:
                p = document.paragraph()
                edit = actionRequireAuthentication(
                    label = 'Edit',
                    sentry = director.sentry,
                    actor = 'createinstrumentfromtemplate',
                    routine = 'edit',
                    id = instrument.id,
                    )
                link = action_link(edit, director.cgihome)
                p.text = [
                    '%s this instrument.' % link,
                    ]

            # create new instrument from this template link
            p = document.paragraph()
            newinstrument = actionRequireAuthentication(
                sentry = director.sentry,
                actor = 'createinstrumentfromtemplate',
                routine = 'start',
                label = 'Create a new instrument',
                template = instrument.id,
                )
            link = action_link(newinstrument, director.cgihome)
            p.text = [
                '%s using this instrument as template.' % link,
                ]

        return page


    def view3d(self, director):
        try:
            page = director.retrieveSecurePage( 'instrument' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        instrument = self._getinstrument(director)

        # populate the main column
        title = 'Instrument #%s: %s' % (instrument.id, instrument.short_description)
        document = main.document(title=title)
        document.description = ''
        document.byline = 'byline?'

        from InstrumentShapeRenderer import Renderer
        renderer = Renderer(director.clerk.db)
        solid = renderer.render(instrument)

        import vnf.content
        view = vnf.content.solidView3D(solid, width=400, height=400)
        
        document.contents.append( view )
        return page


    def listall(self, director):
        try:
            page = director.retrieveSecurePage( 'instrument' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        # populate the main column
        document = main.document(title='Instruments')
        document.description = ''
        document.byline = 'byline?'

        # featured instruments
        featured_list_doc = document.document(title="Featured Instruments")
        
        # retrieve id:record dictionary from db
        clerk = director.clerk
        where = "status='online' and creator='vnf'"
        instruments = clerk.indexInstruments(where=where).values()
        _sortByCategory(instruments)

        # images
        images = [
            (os.path.join( 'instruments', i.id, 'middle-size-icon.png'),
             actionRequireAuthentication(
                 actor = 'instrument',
                 sentry = director.sentry,
                 label = '', routine = 'show',
                 arguments = { 'id': i.id }
                 )
             )
            for i in instruments ]


        # a gallery of instruments
        gallery  = vnf.content.slidableGallery( images )
        featured_list_doc.contents.append( gallery )

        p = featured_list_doc.paragraph()
        p.text = ['']

        my_list_doc = document.document(title="My Instruments")
        p = my_list_doc.paragraph()
        action = actionRequireAuthentication(
            label = 'here',
            sentry = director.sentry,
            actor = 'instrument', routine = 'listmyinstruments',
            )
        link = action_link(action, director.cgihome)
        p.text = [
            'To view your own instruments, please click %s' % link,
            ]
        return page


    def listmyinstruments(self, director):
        try:
            page = director.retrieveSecurePage( 'instrument' )
        except AuthenticationError, err:
            return err.page
        
        main = page._body._content._main

        # populate the main column
        document = main.document(title='My instruments')
        document.description = ''
        document.byline = 'byline?'

        clerk = director.clerk
        where = "status='online' and creator='%s'" % director.sentry.username
        myinstruments = clerk.indexInstruments(where=where).values()
        _sortByCategory(myinstruments)
        table = instrumenttable(myinstruments, director)
        document.contents.append(table)
        
        return page


    def _obsolete_edit(self, director):
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


    def _isAccessible(self, instrument, director):
        accesscontrol = director.accesscontrol
        username = director.sentry.username
        user = director.clerk.getUser(username)
        return accesscontrol.checkInstrumentPrivilege(user, instrument)
        
        
    def _imageStore(self, instrument):
        return os.path.join( 'instruments', instrument.id )


    def _configure(self):
        base._configure(self)
        self.id = self.inventory.id
        form_received = self.form_received = self.inventory.form_received
        if form_received.name == 'instrument':
            form_received.inventory.id = self.id
            pass
        return


    pass # end of Instrument


def _sortByCategory( instruments ):
    t = {True:-1, False:1}
    def compare( x, y ):
        if x.category == y.category: return t[x.id < y.id]
        return t[x.category < y.category]
    instruments.sort( compare )
    return


def build_run( instrument ):
    from InstrumentSimulationRunBuilder import Builder
    return Builder().render(instrument)



def instrumenttable(instruments, director):
    from vnf.content.table import Model, View, Table
    class model(Model):
        
        name = Model.Measure(name='name', type='text')
        category = Model.Measure(name='category', type='text')
        long_description = Model.Measure(name='long_description', type='text')

    class D: pass
    def _showinstrument_link(label, id, director):
        action = actionRequireAuthentication(
            label = label,
            sentry = director.sentry,
            actor = 'instrument', routine = 'show',
            id = id,
            )
        return action_link(action, director.cgihome)
    def _name(instrument):
        label = instrument.short_description
        id = instrument.id
        return _showinstrument_link(label, id, director)
    import operator
    generators = {
        'name': _name,
        'category': operator.attrgetter( 'category' ),
        'long_description': operator.attrgetter( 'long_description' ),
        }
    def d(s):
        r = D()
        for attr, g in generators.iteritems():
            value = g(s)
            setattr(r, attr, value)
            continue
        return r
    data = [d(s) for s in instruments]

    class view(View):
        
        columns = [
            View.Column(id='col1',label='Name', measure='name'),
            View.Column(id='col2',label='Category', measure='category'),
            View.Column(id='col3',label='Description', measure='long_description'),
            ]

        editable = False

    table = Table(model, data, view)
    return table


# version
__id__ = "$Id$"

# End of file 
