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

    def onUploader(self, uploader):
        configurations = self.configurations
        home = configurations['home']
        cgihome = configurations['cgihome']

        stylesheets = ['uploader.css']
        csscode = []
        for stylesheet in stylesheets:
            csscode.append( '<link rel="stylesheet" type="text/css" href="%s/css/%s" />' % (
                home, stylesheet) )
            continue

        htmlcode = []

        htmlcode.append('<div class="formfield">')
        
        htmlcode.append('<div>')
        htmlcode.append('<label for="%s">%s</label>' % (uploader.id, uploader.label))
        htmlcode.append('</div>')
        
        if uploader.error:
            htmlcode.append('<div class="error">%s</div>' % uploader.error)
        if uploader.help:
            htmlcode.append('<div class="formfieldHelp">%s</div>' % uploader.help)
        htmlcode.append( '<div id="%s"> </div>' % uploader.id)
        htmlcode.append('</div>')

        return csscode + htmlcode



class JSMill:

    def onUploader(self, uploader):
        configurations = self.configurations
        cgihome = configurations['cgihome']

        includes = [
            'jquery/jquery.js',
            'jquery/elementFactory.js',
            'jquery/ajaxupload.3.0.js',
            'jquery/uploader.js',            
            ]
        self.include(scripts=includes)

        action = uploader.action
        parameters = {
            'actor': action.actor,
            'routine': action.routine,
            'sentry.username': action.sentry.username,
            'sentry.ticket': action.sentry.ticket,
            }
        for k,v in action.arguments.iteritems():
            parameters[ '%s.%s' % (action.actor, k) ] = v
        
        self.writemain( '$("#%s").uploader( "%s", %s );' % (
            uploader.id, cgihome, parameters) )
        
        return
        


# version
__id__ = "$Id$"

# End of file 
