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


from opal.weaver.PageMill import PageMill as base

class PageMill(base):

    def __init__(self, configurations):
        
        base.__init__(self)

        from TagMill import TagMill
        self.tagger = TagMill()

        from HeadMill import HeadMill
        self.headMill = HeadMill(self.tagger)

        from BodyMill import BodyMill
        self.bodyMill = BodyMill(self.tagger, configurations)
        return



# version
__id__ = "$Id$"

# End of file 
