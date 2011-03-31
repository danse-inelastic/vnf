#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

"""
Interface changes:
    "html"  -> "a"
    "a"     -> "link"

Added:
    "div"
"""

import luban.content as lc
OPTIONS = ["a", "div", "link", "p"]

class Message:
    """
    Data structure for job and delivery status.
    
    """
    def __init__(self, text="", id = None, Class = None):
        self._text   = text
        self._id        = id        # CSS id            
        self._class     = Class     # CSS class         
        self._onload    = None
        self._htmllink  = None      # for HtmlDocument  
        self._islink    = False
        self._state     = ""        # State of the status


    def string(self, format=None):
        """
        Returns formatted status text

        Parameters:
            format  - format in which to display the text
                None    - No format (string)
                "a"     - luban HtmlDocument with <a> tag
                "div"   - luban HtmlDocument with <div> tag
                "link"  - luban Link (action link)
                "p"     - luban Paragraph
                ""
        """
        if format in OPTIONS:
            return getattr(self, format)()

        return self._text


    def setHtmlLink(self, text, link):       # Need to pass Class or id?
        self._text   = text
        self._htmllink  = link


    def setLink(self, text, onload = None):  # Need to pass Class or id?
        self._text   = text
        self._onload    = onload


    def setClass(self, Class):
        self._class = Class


    def text(self, text):
        "Set status text"
        self._text   = text
        

    def set(self, state, text=None):
        "Sets state of the status"
        self._state     = state
        if text:
            self._text   = text


    def get(self, state=None):
        "Returns state of the status"
        return self._state


    def stateLabel(self):
        "Returns state and corresponding description"
        return (self._state, self._text)


    def tag(self, name):
        attr    = []
        if self._htmllink and name == "a":
            attr.append("href='%s'" % self._htmllink)

        if self._class:
            attr.append("class='%s'" % self._class)

        if self._id:
            attr.append("id='%s'" % self._id)

        s   = " ".join(attr)
        return lc.htmldocument(text="<%s %s>%s</%s>" % (name, s, self._text, name))


    def a(self):
        return self.tag("a")

    def div(self):
        return self.tag("div")

    def link(self):
        link    = lc.link(label=self._text)
        if self._onload:
            link.onload = self._onload

        if self._class:
            link.Class  = self._class
            
        return link


    def p(self):
        paragraph    = lc.paragraph(text=self._text)
        if self._class:
            paragraph.Class  = self._class

        return paragraph


def test():
    status  = Message(text="Hello world", Class="cool", id="real")
    print status.string()
    print status.string("a").text
    print status.string("div").text
    print status.string("link").label
    print status.string("p").text


if __name__ == "__main__":
    test()

__date__ = "$Dec 20, 2009 12:06:28 PM$"



