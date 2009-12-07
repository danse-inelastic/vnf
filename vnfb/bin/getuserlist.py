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


from pyre.applications.Script import Script


class DbApp(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", default='clerk')
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        import pyre.idd
        idd = pyre.inventory.facility('idd-session', factory=pyre.idd.session, args=['idd-session'])
        idd.meta['tip'] = "access to the token server"


    def main(self, *args, **kwds):
        db = self.clerk.db
        from vnf.dom.User import User

        users = db.query(User).all()
        for user in users:
            print "%s <%s>" % (user.fullname, user.email)
        return


    def __init__(self):
        Script.__init__(self, 'initdb')
        self.db = None
        return


    def _configure(self):
        Script._configure(self)
        self.clerk = self.inventory.clerk
        self.clerk.director = self
        return


    def _init(self):
        Script._init(self)

        self.db = self.clerk.db
        self.idd = self.inventory.idd

        # initialize table registry
        import vnf.dom
        vnf.dom.register_alltables()

        # id generator
        def guid(): return '%s' % self.idd.token().locator
        import vnf.dom
        vnf.dom.set_idgenerator( guid )
        return


    def _getPrivateDepositoryLocations(self):
        return ['../config']
    


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
