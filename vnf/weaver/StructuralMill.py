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


from opal.weaver.StructuralMill import StructuralMill  as base
from DocumentMill import DocumentMill


class StructuralMill(DocumentMill, base):
    
    def __init__(self, tagger, configurations):
        DocumentMill.__init__(self, tagger, configurations)
        return


# version
__id__ = "$Id$"

# End of file 
