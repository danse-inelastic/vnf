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

class QEStatus:
    """
    Data structure for job and delivery status.
    
    """
    def __init__(self, message="", id = None, Class = None):
        self._message   = message
        self._id        = id        # CSS id            
        self._class     = Class     # CSS class         
        self._onload    = None
        self._htmllink  = None      # for HtmlDocument  
        self._islink    = False
        self._state     = ""        # State of the status


    def string(self, format=None):
        """
        Returns formatted status message

        Parameters:
            format  - format in which to display the message
                None    - No format (string)
                "a"     - luban HtmlDocument with <a> tag
                "div"   - luban HtmlDocument with <div> tag
                "link"  - luban Link (action link)
                "p"     - luban Paragraph
                ""
        """
        if format in OPTIONS:
            return getattr(self, format)()

        return self._message


    def setHtmlLink(self, message, link):       # Need to pass Class or id?
        self._message   = message
        self._htmllink  = link


    def setLink(self, message, onload = None):  # Need to pass Class or id?
        self._message   = message
        self._onload    = onload

    
    def message(self, message):
        "Set status message"
        self._message   = message
        

    def set(self, state, message=None):
        "Sets state of the status"
        self._state     = state
        if message:
            self._message   = message


    def get(self, state):
        "Returns state of the status"
        return self._state


    def tag(self, name):
        attr    = []
        if self._htmllink and name == "a":
            attr.append("href='%s'" % self._htmllink)

        if self._class:
            attr.append("class='%s'" % self._class)

        if self._id:
            attr.append("id='%s'" % self._id)

        s   = " ".join(attr)
        return lc.htmldocument(text="<%s %s>%s</%s>" % (name, s, self._message, name))


    def a(self):
        return self.tag("a")

    def div(self):
        return self.tag("div")

    def link(self):
        link    = lc.link(label=self._message)
        if self._onload:
            link.onload = self._onload

        if self._class:
            link.Class  = self._class
            
        return link


    def p(self):
        paragraph    = lc.paragraph(text=self._message)
        if self._class:
            paragraph.Class  = self._class

        return paragraph


def test():
    status  = QEStatus(message="Hello world", Class="cool", id="real")
    print status.string()
    print status.string("a").text
    print status.string("div").text
    print status.string("link").label
    print status.string("p").text


if __name__ == "__main__":
    test()

__date__ = "$Dec 20, 2009 12:06:28 PM$"



