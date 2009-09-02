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


class Plot_2DMill:


    def onPlot_2D(self, plot):
        home = self.configurations['home']
        cgihome = self.configurations['cgihome']
        javascriptpath = os.path.join( home, 'javascripts' )
        
        csscode = []
        #csscode.append( '<link rel="stylesheet" type="text/css" href="%s/css/flot/layout.css" />' % home )

        htmlcode = []
        gid = id(plot)
        htmlcode.append( '<div id="%s">' % gid )
        htmlcode.append( '</div>' )

        codes = csscode + htmlcode
        return codes


    pass # end of DocumentMill



class JSMill:


    def onPlot_2D(self, plot):
        includes = [
            'jquery/jquery.js',
            'jquery/jquery.flot.js',
            'jquery/elementFactory.js',
            'jquery/plotxy.js',
            ]
        self.include(scripts=includes)

        jsdatacode = _jsdatacode( plot.data )
        self.writemain(jsdatacode)

        gid = id(plot);
        self.writemain('$("#%s").plotxy(X,Y, {});' % gid);
        
        return

def _jsdatacode( data ):
    x, y = data
    return 'X=%s; Y=%s;' % (list(x),list(y))



import os
from vnf.weaver import action_href


# version
__id__ = "$Id$"

# End of file 
