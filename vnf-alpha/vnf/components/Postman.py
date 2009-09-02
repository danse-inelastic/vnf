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


class Postman(Component):


    class Inventory(Component.Inventory):

        import pyre.inventory

        host = pyre.inventory.str(name="host", default="localhost")
        host.meta['tip'] = "the smtp relay hostname"


    def send(self, sender, recipient, msg):

        import smtplib
        server = smtplib.SMTP(self.host)
        # server.set_debuglevel(9)
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
                   
        return


    def __init__(self, name=None):
        if name is None:
            name = "postman"
        super(Postman, self).__init__(name, facility='postman')

        self.host = None
        
        return


    def _configure(self):
        super(Postman, self)._configure()
        self.host = self.inventory.host
        return


# version
__id__ = "$Id: Postman.py,v 1.2 2007-10-07 05:49:26 aivazis Exp $"

# End of file 
