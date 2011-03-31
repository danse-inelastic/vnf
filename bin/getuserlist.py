#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from luban.applications.UIApp import UIApp as base


class DbApp(base):


    class Inventory(base.Inventory):

        import pyre.inventory


    def main(self, *args, **kwds):
        db = self.clerk.db
        from vnfb.dom.User import User

        users = db.query(User).all()
        for user in users:
            print "%s <%s>" % (user.fullname, user.email)
        return


    def __init__(self):
        super(DbApp, self).__init__('getuserlist')
        return


    def _defaults(self):
        super(DbApp, self)._defaults()
        return


    def _getPrivateDepositoryLocations(self):
        return ['../config', '../content/components', '/tmp/luban-services']
    


def main():
    import journal
    journal.debug('db').activate()
    app = DbApp()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
