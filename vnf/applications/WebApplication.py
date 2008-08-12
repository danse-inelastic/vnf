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


class AuthenticationError(Exception):

    def __init__(self, page):
        self.page = page
        Exception.__init__(self, page)
        return
    pass
    

from opal.applications.WebApplication import WebApplication as Base


class WebApplication(Base):


    class Inventory(Base.Inventory):
        
        import opal.inventory
        import pyre.inventory

        # properties
        db = pyre.inventory.str(name='db', default='vnf')
        db.meta['tip'] = "the name of the database"

        dbwrapper = pyre.inventory.str(name='dbwrapper', default='psycopg')
        dbwrapper.meta['tip'] = "the python package that provides access to the database back end"

        # components
        actor = opal.inventory.actor(default="login")
        actor.meta['tip'] = "the component that defines the application behavior"

        import pyre.idd
        idd = pyre.inventory.facility('idd-session', factory=pyre.idd.session, args=['idd-session'])
        idd.meta['tip'] = "access to the token server"

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnf.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        scribe = pyre.inventory.facility(name="scribe", factory=vnf.components.scribe)
        scribe.meta['tip'] = "the component responsible for rendering the generated reports"

        csaccessor = pyre.inventory.facility( name='csaccessor', factory = vnf.components.ssher)
        csaccessor.meta['tip'] = 'computing server accessor'

        debug = pyre.inventory.bool(name="debug", default=True)
        debug.meta['tip'] = "suppress some html output for debugging purposes"

        imagepath = pyre.inventory.str(name='imagepath', default = '/vnfBK/images' )
        javascriptpath = pyre.inventory.str(name='javascriptpath', default = '/vnfBK/javascripts' )
        javapath = pyre.inventory.str(name='javapath', default = '/java' )


    def main(self, *args, **kwds):
        if self.debug:
            from configurationSaver import toPml
            from os import environ
            user = environ.get('USER') or 'webserver'
            toPml(self, '/tmp/main-debug-%s.pml' % user)
        super(WebApplication, self).main(*args, **kwds)
        return


    def retrievePage(self, name):
        page = super(WebApplication, self).retrievePage(name)
        if page:
            return page

        if self.debug:
            self._debug.log( "*** could not locate page %r" % name )
            return
        
        page = super(WebApplication, self).retrievePage("error")
        return page


    def retrieveSecurePage(self, name):
        # check that the username is allowed
        activeUsers = self.clerk.indexActiveUsers()
        if self.sentry.username not in activeUsers:
            raise AuthenticationError, self.retrievePage( "invalid-user" )
        
        # check that the password is valid
        ticket = self.sentry.authenticate()
        if ticket is None:
            raise AuthenticationError, self.retrievePage( 'authentication-error' )

        # all good; grab the page
        return self.retrievePage(name)


    def __init__(self, name):
        Base.__init__(self, name)

        # turn on the info channel
        self._info.activate()

        # access to the token server
        self.idd = None

        # access to the data retriever
        self.clerk = None

        # access to the data renderer
        self.scribe = None

        # debugging mode
        self.debug = False

        return


    def _configure(self):
        super(WebApplication, self)._configure()

        self.idd = self.inventory.idd
        self.clerk = self.inventory.clerk
        self.clerk.director = self
        self.scribe = self.inventory.scribe
        self.debug = self.inventory.debug
        self.csaccessor = self.inventory.csaccessor

        import vnf.weaver
        configurations = {
            'home': self.home,
            'cgihome':self.cgihome,
            'imagepath':self.inventory.imagepath,
            'javascriptpath':self.inventory.javascriptpath,
            'javapath':self.inventory.javapath,
            }
        self.pageMill = vnf.weaver.pageMill( configurations )
        return


    def _init(self):
        super(Base, self)._init()

        # connect to the database
        import pyre.db
        self.db = pyre.db.connect(database=self.inventory.db, wrapper=self.inventory.dbwrapper)

        # initialize the accessors
        self.clerk.db = self.db

        return


    def _getPrivateDepositoryLocations(self):
        return ['../content', '../config']


import journal
journal.debug('curator').activate()

# version
__id__ = "$Id: WebApplication.py,v 1.3 2007-08-30 16:46:08 aivazis Exp $"

# End of file 
