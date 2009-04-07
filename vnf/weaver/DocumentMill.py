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


from DocumentMillExtensions import extensions
from _utils import Inherited
Extension = Inherited(extensions)

from opal.weaver.DocumentMill import DocumentMill as base
class DocumentMill(Extension, base):

    def __init__(self, tagger, configurations):
        base.__init__(self, tagger)
        self.configurations = configurations
        return

    pass # end of DocumentMill


# version
__id__ = "$Id$"

# End of file 
