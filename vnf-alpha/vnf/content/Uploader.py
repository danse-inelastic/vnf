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


class Uploader:

    def __init__(self, action, label='Uploader', help='', error = '', id=''):
        if not id:
            id = __builtins__['id'](self)
        self.id = id
        
        self.action = action
        self.label = label
        self.help = help
        self.error = error
        return

    def identify(self, visitor):
        return visitor.onUploader(self)


# version
__id__ = "$Id$"

# End of file 
