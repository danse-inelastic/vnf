#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

# a temporary solution to add raw javascript codes

class JSsnippet:

    def __init__(self, includes=[], main=[], stylesheets=[]):
        self.includes = includes
        self.main = main
        self.stylesheets = stylesheets
        return


    def identify(self, visitor):
        return visitor.onJSsnippet(self)
    

# version
__id__ = "$Id$"

# End of file 
