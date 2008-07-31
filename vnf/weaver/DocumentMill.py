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


from opal.weaver.DocumentMill import DocumentMill as base
from ActionLinkRenderer import ActionLinkRenderer


class DocumentMill(ActionLinkRenderer, base):

    def __init__(self, tagger, configurations):
        base.__init__(self, tagger)
        
        cgihome = configurations['cgihome']
        ActionLinkRenderer.__init__(self, cgihome)

        from TreeViewMill import TreeViewMill
        self.treeviewmill = TreeViewMill(configurations)
        
        from AccordionMill import AccordionMill
        self.accordionMill = AccordionMill(configurations)
        return


    def onTreeView(self, treeview):
        return self.treeviewmill.render( treeview )


    def onAccordion(self, accordion):
        return self.accordionMill.render( accordion )

    pass # end of DocumentMill


# version
__id__ = "$Id$"

# End of file 
