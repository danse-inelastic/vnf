#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from pyre.weaver.mills.XMLMill import XMLMill


class Renderer(XMLMill):


    def render(self, jnlp):
        document = self.weave(jnlp)
        return document


    # handlers

    def onJnlp(self, jnlp):
        self._write('<?xml version="1.0" encoding="utf-8"?>')

        tag = 'jnlp'
        props = {
            'spec': jnlp.specification,
            'codebase': jnlp.codebase,
            'href': jnlp.href,
            }
        self.startElement(tag, props)
        self._indent()

        subelements = [
            jnlp.information,
            jnlp.security,
            ]
        for elem in subelements:
            elem.identify(self)
            continue

        self.startElement('resources')
        self._indent()
        for resource in jnlp.resources:
            resource.identify(self)
            continue
        self._outdent()
        self.endElement('resources')

        self.drawElement('application-desc', {'main-class':jnlp.main_class})

        self._outdent()
        self.endElement(tag)
        return


    def onInformation(self, information):
        tag = 'information'
        self.startElement(tag)
        self._indent()
        
        self.drawElement('title', content=[information.title])
        self.drawElement('vendor', content=[information.vendor])
        self.drawElement('homepage', {'href': information.homepage})

        for kind, texts in information.descriptions.iteritems():
            props = {}
            if kind: props['kind'] = kind
            self.drawElement('description', props, texts)
            continue
            
        for kind, href in information.icons.iteritems():
            props = {}
            if kind: props['kind'] = kind
            props['href'] = href
            self.drawElement('icon', props)
            continue

        for opt in information.options:
            self.drawElement(opt)
            continue

        self._outdent()
        self.endElement(tag)
        return


    def onSecurity(self, security):
        #hack
        self.drawElement('security', content=['<all-permissions/>'])
        return


    def onJ2SE(self, j2se):
        props = {
            'version': j2se.version,
            }
        self.drawElement('j2se', props)
        return


    def onJar(self, jar):
        props = {
            'href': jar.href,
            'main': jar.main,
            }
        self.drawElement('jar', props)
        return


    def onExtension(self, extension):
        props = {
            'href': extension.href,
            }
        self.drawElement('extension', props)
        return


    def drawElement(self, tag, properties={}, content=[]):
        if content:
            self.startElement(tag, properties)
            self._indent()
            for line in content: self._write(line)
            self._outdent()
            self.endElement(tag)
        else:
            s = '<'+tag+' '
            s += _propsStr(properties)
            s += '/>'
            self._write(s)
        return
    

    def startElement(self, tag, properties={}):
        s = '<'+tag+' '
        s += _propsStr(properties)
        s += '>'
        self._write(s)
        return


    def endElement(self, tag):
        s = '</'+tag+'>'
        self._write(s)
        return


    def _indent(self): self._indent_level+=1
    def _outdent(self): self._indent_level-=1


    def _write(self, line):
        s = self._indent_level * self._indent_characters + line
        self._rep.append(s)
        return

    
    def __init__(self):
        XMLMill.__init__(self)
        self._indent_level = 0
        self._indent_characters = '  '
        return


    def _renderDocument(self, document):
        return document.identify(self)
    


def _propsStr(properties):
    words = ['%s="%s"' % (k,v) for k,v in properties.iteritems()]
    return ' '.join(words)

# version
__id__ = "$Id"

# End of file 
