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


from opal.content.Document import Document as base
class Dialog(base):

    def __init__(self, title, description="", **kwds):

        # get a unique id
        id = kwds.get('id')
        if not id:
            id = __builtins__['id'](self)
        kwds['id'] = self.id = id
        
        super(Dialog, self).__init__(title, description=description, **kwds)
        return

    def identify(self, visitor):
        return visitor.onDialog(self)


# version
__id__ = "$Id$"

# End of file 
