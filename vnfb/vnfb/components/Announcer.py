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


class Announcer(Component):


    class Inventory(Component.Inventory):

        import pyre.inventory

        host = pyre.inventory.str(name="host", default="localhost")
        host.meta['tip'] = "the smtp relay hostname"


    def createEnvelop(self, source, destination, subject):
        from email.MIMEMultipart import MIMEMultipart

        envelop = MIMEMultipart()
        envelop['From'] = source
        envelop['To'] = destination
        envelop['Subject'] = subject
        envelop.epilogue = '' # make sure it ends with a newline

        return envelop


    def createBody(self, text):
        from email.MIMEText import MIMEText
        body = MIMEText(_text=text, _charset='utf-8')
        return body


    def createAttachments(self, filenames):
        from email.MIMEText import MIMEText

        attachments = []

        for name in filenames:
            path, base = os.path.split(name)
            source = file(name, "r")
            attachment = MIMEText(source.read())
            attachment.add_header('Content-disposition', 'attachment', filename=base)
            attachments.append(attachment)

        return attachments


    def __init__(self, name=None):
        if name is None:
            name = "announcer"
        super(Announcer, self).__init__(name, facility='announcer')
        
        return


    def _configure(self):
        super(Announcer, self)._configure()
        return


# version
__id__ = "$Id: Announcer.py,v 1.2 2008-09-01 20:28:14 aivazis Exp $"

# End of file 
