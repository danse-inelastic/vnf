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
        cod = pyre.inventory.facility(name='cod', default='cod')


    def main(self, *args, **kwds):
        cod = self.inventory.cod
        try:
            cod.connect()
            print "Good"
        except:
            import traceback
            tb = traceback.format_exc()
            cod.sendServerDownAlert(tb, director=self)
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
__id__ = "$Id$"

# End of file 
