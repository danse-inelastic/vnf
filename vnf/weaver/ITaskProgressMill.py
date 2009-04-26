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

    def onITaskProgress(self, widget):
        configurations = self.configurations
        home = configurations['home']
        cgihome = configurations['cgihome']

        stylesheets = ['jquery-ui/smoothness/ui.all.css']
        csscode = []
        for stylesheet in stylesheets:
            csscode.append( '<link rel="stylesheet" type="text/css" href="%s/css/%s" />' % (
                home, stylesheet) )
            continue
        csscode.append('''
<style type="text/css">
.ui-progressbar-value{ background-image: url(javascripts/jquery/ui/css/images/pbar-ani.gif); }
</style>
''')
        
        htmlcode = []
        htmlcode.append('<div id="%s"></div>' % widget.id)
        
        return csscode + htmlcode



class JSMill:

    def onITaskProgress(self, widget):
        configurations = self.configurations
        cgihome = configurations['cgihome']
        sentry = widget.sentry

        includes = [
            'jquery/ui/ui.core.js',
            'jquery/ui/ui.draggable.js',
            'jquery/ui/ui.resizable.js',
            'jquery/ui/ui.dialog.js',
            'jquery/ui/ui.progressbar.js',
            'jquery/itask.js',
            ]
        self.include(scripts=includes)

        from vnf.components.Actor import actionRequireAuthentication
        from vnf.weaver import action_href
        startaction = actionRequireAuthentication(
            actor = 'itask',
            routine = 'start',
            id = widget.taskid,
            sentry = sentry,
            arguments = {'response-type': 'json'},
            )
        startaction_url = action_href(startaction, cgihome)

        refreshaction = actionRequireAuthentication(
            actor = 'itask',
            routine = 'getProgress',
            id = widget.taskid,
            sentry = sentry,
            arguments = {'response-type': 'json'},
            )
        refreshaction_url = action_href(refreshaction, cgihome)

        finished_callback = widget.finished_callback
        title = widget.label
        options = '''{
            updateurl: "%(refreshaction_url)s",
            starturl: "%(startaction_url)s",
            callback: %(finished_callback)s,
            title: "%(title)s",
            }''' % locals()
        self.writemain(
            '$("#%s").itaskmonitor("create", %s);' % (widget.id, options)
            )
        return
        


# version
__id__ = "$Id$"

# End of file 
