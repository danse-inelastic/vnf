#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                               Orthologue, Ltd.
#                      (C) 2004-2006  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.components.Component import Component


class Announcement(Component):


    def announce(self, app, postman=None, announcer=None):

        if app and postman is None:
            postman = app.postman

        if app and announcer is None:
            announcer = app.announcer
        
        for recipient, subs in self.recipients.iteritems():
            self._debug.log("sending email to %s" % recipient)

            # create the evelop
            envelop = announcer.createEnvelop(self.sender, recipient, self.subject)
            
            # attach the message body
            text = "\n".join([ line % subs for line in self.text ])
            body = announcer.createBody(text)
            envelop.attach(body)
            
            # send the email
            postman.send(self.sender, recipient, envelop)

        return


    def __init__(self, name=None):
        if name is None:
            name = "announcement"
        super(Announcement, self).__init__(name, "announcement")

        self.sender = ""
        self.subject = ""
        self.text = []
        self.recipients = {}

        return


# version
__id__ = "$Id: Announcement.py,v 1.3 2007-10-07 05:48:20 aivazis Exp $"

# End of file 
