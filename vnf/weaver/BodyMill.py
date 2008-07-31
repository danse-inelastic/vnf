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


from opal.weaver.BodyMill import BodyMill  as base


class BodyMill(base):
    
    def __init__(self, tagger, configurations):
        base.__init__(self, tagger)
        
        from StructuralMill import StructuralMill
        self.structuralMill = StructuralMill(tagger, configurations)
        return


# version
__id__ = "$Id$"

# End of file 
