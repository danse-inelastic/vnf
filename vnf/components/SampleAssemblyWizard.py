# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from Actor import action_link, action, actionRequireAuthentication, AuthenticationError

from FormActor import FormActor as base

class SampleAssemblyWizard(base):

    class Inventory(base.Inventory):

        import pyre.inventory
        
        id = pyre.inventory.str( 'id', default = '')
        
        pass # end of Inventory


    def default(self, director):
        return self.new( director )


    def new(self, director):
        'new sample assembly. wizard step 1'
        try:
            page = director.retrieveSecurePage( 'sampleassembly' )
        except AuthenticationError, err:
            return err.page

        record = new_sampleassembly( director )

        main = page._body._content._main

        # populate the main column
        document = main.document(title='Sample Assembly Builder')
        document.description = (
            'A sample assembly is a collection of neutron scatterers. '\
            'For example, it can consist of a main sample, '\
            'a sample container, and a furnace.\n'\
            )
        document.byline = 'byline?'

        # form
        formcomponent = self.retrieveFormToShow( 'sampleassembly' )
        formcomponent.inventory.id = record.id
        formcomponent.director = director

        form = document.form(
            name='sampleassembly',
            legend= formcomponent.legend(),
            action=director.cgihome)

        # specify action
        action = actionRequireAuthentication(
            actor = 'sampleassemblywizard', sentry = director.sentry,
            label = '', routine = 'new1',
            arguments = { 'id': record.id,
                          'form-received': formcomponent.name } )
        from vnf.weaver import action_formfields
        action_formfields( action, form )

        # expand the form with fields of the data object that is being edited
        formcomponent.expand( form )

        # ok button
        submit = form.control(name="submit", type="submit", value="next")
        
        return page


    def new1(self, director):
        try:
            page = director.retrieveSecurePage( 'sampleassembly' )
        except AuthenticationError, err:
            return err.page

        id = self.inventory.id
        record = director.clerk.getSampleAssembly( id )
        record = director.getHierarchy( record )
        scatterers = record.scatterers

        for scatterer in scatterers:
            p = document.paragraph()
            link = action_link(
                actionRequireAuthentication(
                    'scatterer',
                    director.sentry,
                    routine = 'addscatterer',
                    label = 'add',
                    ),  director.cgihome
                )
            continue

        p = document.paragraph()
        link = action_link(
            actionRequireAuthentication(
                'sampleassemblywizard',
                director.sentry,
                routine = 'addscatterer',
                label = 'add',
                ),  director.cgihome
            )
        p.text = [
            'There is no scatterer in sample assembly at this moment. ',
            'Please %s a scatterer.' % link,
            ]

        return page
    

    def __init__(self, name=None):
        if name is None:
            name = "sampleassemblywizard"
        super(SampleAssemblyWizard, self).__init__(name)
        return




# version
__id__ = "$Id$"

# End of file 
