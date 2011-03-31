# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
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

            # create the envelop
            envelop = announcer.createEnvelop(self.sender, recipient, self.subject)
            
            # attach the message body
            try:
                text = "\n".join([ line % subs for line in self.text ])
            except:
                text = self.text + ['subs: ' + str(subs)]
                text = '\n'.join(text)
            if hasattr(self, 'html'):
                html = "\n".join([ line % subs for line in self.html ])
            else:
                html = None
            body = announcer.createBody(text, html=html)
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
__id__ = "$Id$"

# End of file 
