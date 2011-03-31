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
        port = pyre.inventory.int(name="port", default=0)

        username = pyre.inventory.str(name="username")
        password = pyre.inventory.str(name="password")


    def send(self, sender, recipient, msg):

        import smtplib
        port = self.port
        if port:
            server = smtplib.SMTP(self.host, port=port)
        else: 
            server = smtplib.SMTP(self.host)
        
        self._prepare(server)

        username = self.username
        password = self.password
        if username and password: server.login(username, password)
        
        # server.set_debuglevel(9)
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
                   
        return


    def _prepare(self, server):
        require_tls = ['smtp.gmail.com']
        if self.host in require_tls:
            server.starttls()
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
        self.port = self.inventory.port
        self.username = self.inventory.username
        self.password = self.inventory.password
        return


# version
__id__ = "$Id: Postman.py,v 1.2 2007-10-07 05:49:26 aivazis Exp $"

# End of file 
