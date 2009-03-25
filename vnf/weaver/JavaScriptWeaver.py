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


from JavaScriptWeaverExtensions import extensions
from _utils import Inherited
Extension = Inherited(extensions)

from JavaScriptWeaverBase import JavaScriptWeaverBase as base
class JavaScriptWeaver(Extension, base):

    pass  # end of JavaScriptWeaver


# version
__id__ = "$Id$"

# End of file 
