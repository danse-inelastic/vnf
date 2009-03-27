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



class JavaScriptWeaverBase:

    def __init__(self, configurations):
        self.configurations = configurations

        import journal
        self.debug = journal.debug('javascript-weaver')
        
        self._includes = []
        self._script = []
        self._main = []

        return


    def render(self, document):
        # init main function
        self.startmain()
        
        # jquery main needs jquery
        self.include(script='jquery/jquery.js')
        
        # rendering
        document.identify(self)

        # finalize main function
        self.endmain()

        # join main function to the script
        self._script += self._main

        return self._includes, [self._script]
    

    def writemain(self, line):
        self._main.append(line)
        return


    def write(self, line):
        self._script.append(line)
        return


    def include(self, script='', scripts=[]):
        if script and scripts:
            raise ValueError

        if script: scripts = [script]
        for s in scripts: self._include(s)
        return
    

    def startmain(self):
        self._main.append( '$(function (){')
        return


    def endmain(self):
        self._main.append( '});' )
        return


    def doNothing(self, widget): return


    def onContainer(self, container):
        for tag in container.contents:
            tag.identify(self)
        return


    # page
    onPage = onContainer
    onHead = doNothing

    #body
    onBody = onPageSection = onContainer
    def onPageContent(self, page):
        contents = [
            '_leftColumn',
            '_main',
            '_rightColumn',
            ]
        contents = [getattr(page, attr) for attr in contents]
        contents = filter(lambda elem: elem, contents)

        for tag in contents:
            tag.identify(self)
        return
    onLiteral = onParagraph = onPreformatted = doNothing

    #structural
    onPortlet = onDocument = onContainer
    onBanner = onLogo = onPersonalTools = onPortlet = onPortletContent = doNothing

    #document
    onButton = onControlBoxLine = onFormControl = onFormField = onFormHiddenInput \
               = onInput = onSelector = onTextArea \
               = doNothing
    onForm = onControlBox = onContainer


    def _include(self, script):
        configurations = self.configurations
        javascriptpath = configurations['javascriptpath']
        include = os.path.join(javascriptpath, script)
        if include not in self._includes:
            self._includes.append(include)
        return


    pass  # end of JavaScriptWeaverBase


import os


# version
__id__ = "$Id$"

# End of file 
