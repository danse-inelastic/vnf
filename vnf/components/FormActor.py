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


from Actor import *


class FormActor(Actor):

    '''
    A special kind of actor.

    It can accept inputs of a form submitted by the previous
    action, and create a new form.
    '''

    class Inventory( Actor.Inventory ):

        import vnf.inventory

        from Form import Form
        form_received = vnf.inventory.form(
            'form-received', family = 'form', default = 'empty' )

        pass # end of Inventory


    def processFormInputs(self, director):
        form_received = self.form_received
        if form_received is None:
            self._debug.log( 'no form received' )
            return
        form_received.director = director
        return form_received.processUserInputs()


    def retrieveFormToShow(self, name, *args):
        form = self.retrieveComponent(
            name, factory='form', args = list(args),  vault=['forms'])
        return form


    def _configure(self):
        Actor._configure(self)
        self.form_received = self.inventory.form_received
        return


from Form import InputProcessingError


# version
__id__ = "$Id$"

# End of file 
