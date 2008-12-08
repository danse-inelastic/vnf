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
        htmlcode.append( '''
    <div style="float:left">
      <div id="placeholder" style="width:500px;height:300px"></div>
    </div>
    
    <div id="miniature" style="float:left;margin-left:20px;margin-top:50px">
      <div id="overview" style="width:166px;height:100px"></div>

      <p id="overviewLegend" style="margin-left:10px"></p>
    </div>
''')
        htmlcode.append( '</div>' )

        includes = []
        includes.append( '<SCRIPT src="%s/jquery/jquery.js"></SCRIPT>' % javascriptpath )
        includes.append( '<SCRIPT src="%s/jquery/jquery.flot.js"></SCRIPT>' % javascriptpath )

        jscode = []
        jsdatacode = _jsdatacode( plot.data )
        jscode.append('''
$(function () {
    %s;

    function getYLimits() {
        var min = Y[0], max = Y[0];
        
        for (var i=1; i<Y.length; i+=1) {
            if (Y[i]<min) min = Y[i];
            if (Y[i]>max) max = Y[i];
        }
        return {"min": min, "max": max}
    }
    
    // setup plot
    function getData(x1, x2) {
        var d = [];
        for (var i = 0; i < X.length; i += 1) {
            if (X[i] >= x1 && X[i] <= x2) 
                d.push([X[i], Y[i]]);
        }
        return [
            { label: "", data: d }
        ];
    }

    var options = {
        legend: { show: false },
        lines: { show: true },
        points: { show: true },
        yaxis: { ticks: 10 },
        selection: { mode: "xy" }
    };

    var startData = getData(X[0], X[X.length-1]);
    var ylimits = getYLimits();
    
    var plot = $.plot($("#placeholder"), startData, options);

    // setup overview
    var overview = $.plot($("#overview"), startData, {
        legend: { show: true, container: $("#overviewLegend") },
        lines: { show: true, lineWidth: 1 },
        shadowSize: 0,
        xaxis: { ticks: 4 },
        yaxis: { ticks: 3, min: ylimits.min, max: ylimits.max },
        grid: { color: "#999" },
        selection: { mode: "xy" }
    });

    // now connect the two
    var internalSelection = false;
    
    $("#placeholder").bind("selected", function (event, area) {
        // clamp the zooming to prevent eternal zoom
        if (area.x2 - area.x1 < 0.00001)
            area.x2 = area.x1 + 0.00001;
        if (area.y2 - area.y1 < 0.00001)
            area.y2 = area.y1 + 0.00001;
        
        // do the zooming
        plot = $.plot($("#placeholder"), getData(area.x1, area.x2),
                      $.extend(true, {}, options, {
                          xaxis: { min: area.x1, max: area.x2 },
                          yaxis: { min: area.y1, max: area.y2 }
                      }));
        
        if (internalSelection)
            return; // prevent eternal loop
        internalSelection = true;
        overview.setSelection(area);
        internalSelection = false;
    });
    $("#overview").bind("selected", function (event, area) {
        if (internalSelection)
            return;
        internalSelection = true;
        plot.setSelection(area);
        internalSelection = false;
    });
});
''' % jsdatacode)
        
        codes = csscode + includes + ['<script>']  + jscode + ['</script>'] + htmlcode
        return codes


    pass # end of DocumentMill


def _jsdatacode( data ):
    x, y = data
    return 'X=%s; Y=%s' % (list(x),list(y))

import os
from vnf.weaver import action_href


# version
__id__ = "$Id$"

# End of file 
