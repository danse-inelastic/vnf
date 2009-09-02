#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2009  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class Button:

    def __init__(self, label, id=None):
        if not id: id = __builtins__['id'](self)
        self.id = id
        self.label = label
        return

    def identify(self, visitor):
        return visitor.onButton(self)


# version
__id__ = "$Id$"

# End of file 
