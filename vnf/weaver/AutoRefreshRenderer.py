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
        timeout = autorefresh.timeout
        # convert to minutes:seconds
        minutes, seconds = self._decompose(timeout)
        limitstr = '%s:%s' % (minutes, seconds)
        
        home = self.configurations['home']
        cgihome = self.configurations['cgihome']
        javascriptpath = os.path.join( home, 'javascripts' )
        
        csscode = []
        htmlcode = []
        includes = []
        jscode = []
        jscode += ('''
        <!--

        /*
        Auto Refresh Page with Time script
        By JavaScript Kit (javascriptkit.com)
        Over 200+ free scripts here!
        */

        //enter refresh time in "minutes:seconds" Minutes should range from 0 to inifinity. Seconds should range from 0 to 59
        var limit="%s"

        var parselimit=limit.split(":")
        parselimit=parselimit[0]*60+parselimit[1]*1

        function beginrefresh(){
            if (parselimit==1)
            window.location.reload()
            else{
            parselimit-=1
            curmin=Math.floor(parselimit/60)
            cursec=parselimit%60
            if (curmin!=0)
            curtime=curmin+" minutes and "+cursec+" seconds left until page refresh!"
            else
        curtime=cursec+" seconds left until page refresh!"
        window.status=curtime
        setTimeout("beginrefresh()",1000)
        }
        }

        window.onload=beginrefresh
        //-->
        ''' % limitstr).split('\n')
        
        codes = csscode + includes + ['<script>']  + jscode + ['</script>'] + htmlcode
        return codes


    def _decompose(self, seconds):
        seconds  = int(seconds)
        minutes = seconds/60
        seconds = seconds%60
        return minutes, seconds


    pass 
    

# version
__id__ = "$Id$"

# End of file 
