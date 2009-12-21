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

import luban.content as lc

class QEStatus:
    """
    Data structure for job and delivery status"
    """
    def __init__(self, message=""):
        self._message   = message
        self._onload    = None
        self._htmllink  = ""    # for HtmlDocument
        self._islink    = False
        self._class     = ""
        self._state     = ""    # State of the status


    def string(self, format=None):
        """
        Returns formatted status message

        Parameters:
            format  - format in which to display the message
                None    - No format
                "html"  - luban HtmlDocument
                "a"     - luban Link (action link)
                "p"     - luban Paragraph
        """
        
        if format == "a":
            return self._link()

        if format == "html":
            return self._html()

        if format == "p":
            return self._paragraph()

        return self._message


    def setHtmlLink(self, message, link, Class=None):
        self._message   = message
        self._htmllink  = link
        self._class     = Class


    def setLink(self, message, onload = None, Class = None):
        self._message   = message
        self._onload    = onload
        self._class     = Class

    
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

    def _html(self):
        return lc.htmldocument(text="<a href='%s'>%s</a>" % (self._htmllink, self._message))


    def _link(self):
        return lc.link(label=self._message, onload=self._onload, Class=self._class)


    def _paragraph(self):
        return lc.paragraph(text=self._message, Class=self._class)


__date__ = "$Dec 20, 2009 12:06:28 PM$"


