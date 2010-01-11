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

    def _html(self):
        attr    = []
        if self._htmllink:
            attr.append("href='%s'" % self._htmllink)

        if self._class:
            attr.append("class='%s'" % self._class)

        if self._id:
            attr.append("id='%s'" % self._id)

        s   = " ".join(attr)
        return lc.htmldocument(text="<a %s>%s</a>" % (s, self._message))


    def _link(self):
        return lc.link(label=self._message, onload=self._onload, Class=self._class)


    def _paragraph(self):
        return lc.paragraph(text=self._message, Class=self._class)


__date__ = "$Dec 20, 2009 12:06:28 PM$"


