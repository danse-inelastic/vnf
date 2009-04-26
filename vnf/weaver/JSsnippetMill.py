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


class HtmlMill:

    def onJSsnippet(self, snippet):
        return []


class JSMill:

    def onJSsnippet(self, snippet):
        configurations = self.configurations
        cgihome = configurations['cgihome']

        includes = snippet.includes
        self.include(scripts=includes)

        for line in snippet.main:
            self.writemain(line)
            continue

        return


# version
__id__ = "$Id$"

# End of file 
