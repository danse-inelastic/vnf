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
            import traceback
            tb = traceback.format_exc()
            self._sendAlert(tb)
        return

    
    def _sendAlert(self, traceback):
        from vnfb.utils.communications import announce
        announce(self, 'cod-server-down', traceback)
        return
    
    
    def _getPrivateDepositoryLocations(self):
        return ['../config', '../content/components', '/tmp/luban-services']


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
__id__ = "$Id: checkcod.py 3385 2010-12-23 00:05:31Z linjiao $"

# End of file 
