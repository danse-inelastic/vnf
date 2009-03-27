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


class AutoRefreshRenderer:

    def onAutoRefresh(self, autorefresh):
        csscode = []
        htmlcode = []
        codes = csscode + htmlcode
        return codes

    pass



class JSMill:


    def onAutoRefresh(self, autorefresh):
        timeout = autorefresh.timeout
        scripts = [
            'jquery/autorefresh.js',
            ]
        self.include(scripts=scripts)
        self.writemain('autorefresh.start(%s);' % timeout)
        return
    

import os


# version
__id__ = "$Id$"

# End of file 
