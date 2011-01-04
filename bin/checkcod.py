#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from luban.applications.UIApp import UIApp as base


class App(base):


    class Inventory(base.Inventory):

        import pyre.inventory

        host = pyre.inventory.str('host')
        user = pyre.inventory.str('user')
        passwd = pyre.inventory.str('passwd')


    def main(self, *args, **kwds):
        host = self.inventory.host
        user = self.inventory.user
        passwd = self.inventory.passwd
        
        import MySQLdb
        try:
            conn = MySQLdb.connect(
                host = host,
                user = user,
                passwd = passwd,
                db = 'cod',
                )
        except:
            self._sendAlert('cod', sys.exc_info()[0])
        return

    
    def _sendAlert(self, server, error):
        from vnfb.utils.communications import announce
        announce(self, 'cod-server-down', server, error)
        return
    
    
    def __init__(self):
        base.__init__(self, 'checkcod')
        return


import sys


def main():
    import journal
    journal.debug('checkcod').activate()
    app = App()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
