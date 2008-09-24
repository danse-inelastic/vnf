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
        document = main.document(title='Neutron Experiment Wizard: start')
        document.description = ''
        document.byline = 'byline?'

        return page


    def __init__(self, name=None):
        if name is None:
            name = "materialsimulationwizard"
        super(MaterialSimulationWizard, self).__init__(name)
        self.started \
                     = self.name_assigned \
                     = self.instrument_configured \
                     = self.sample_environment_configured \
                     = self.sample_prepared \
                     = self.kernel_configured \
                     = self.allconfigured \
                     = False
        return


    pass # end of MaterialSimulationWizard


from misc import new_id, empty_id, nullpointer

# version
__id__ = "$Id$"

# End of file 
