# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
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

        # components
        actor = opal.inventory.actor(default='nyi')
        actor.meta['tip'] = "the component that defines the application behavior"

        import pyre.idd
        idd = pyre.inventory.facility('idd-session', factory=pyre.idd.session, args=['idd-session'])
        idd.meta['tip'] = "access to the token server"

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnf.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        dds = pyre.inventory.facility(name="dds", factory=vnf.components.dds)
        dds.meta['tip'] = "the component manages data files"

        scribe = pyre.inventory.facility(name="scribe", factory=vnf.components.scribe)
        scribe.meta['tip'] = "the component responsible for rendering the generated reports"

        csaccessor = pyre.inventory.facility( name='csaccessor', factory = vnf.components.ssher)
        csaccessor.meta['tip'] = 'computing server accessor'

        debug = pyre.inventory.bool(name="debug", default=True)
        debug.meta['tip'] = "suppress some html output for debugging purposes"

        imagepath = pyre.inventory.str(name='imagepath', default = '/vnf/images' )
        javascriptpath = pyre.inventory.str(name='javascriptpath', default = '/vnf/javascripts' )
        javapath = pyre.inventory.str(name='javapath', default = '/vnf/java' )


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
        self.dds = self.inventory.dds
        self.dds.director = self
        self.scribe = self.inventory.scribe
        self.debug = self.inventory.debug
        self.csaccessor = self.inventory.csaccessor

        configurations = {
            'home': self.home,
            'cgihome':self.cgihome,
            'imagepath':self.inventory.imagepath,
            'javascriptpath':self.inventory.javascriptpath,
            'javapath':self.inventory.javapath,
            }
        import vnf.weaver
        vnf.weaver.extend_weaver(self.pageMill, configurations )

        if not self.debug: suppressWarnings()
        return


    def _init(self):
        super(WebApplication, self)._init()

        # initialize table registry
        import vnf.dom
        vnf.dom.register_alltables()

        # set id generator for referenceset
        def _id():
            from vnf.components.misc import new_id
            return new_id(self)
        vnf.dom.set_idgenerator(_id)
        return


    def _getPrivateDepositoryLocations(self):
        from os.path import join
        root = '..'
        base = join(root, 'content/base')
        config = join(root, 'config')
        
        from vnf import extensions
        exts = [join(root, 'content', e) for e in extensions]
        
        return [base]+exts+[config]
        


def suppressWarnings():
    import journal
    journal.error('pyre.inventory').deactivate()
    
    import warnings
    categories_to_ignore = [
        DeprecationWarning,
        ]
    for category in categories_to_ignore:
        warnings.filterwarnings('ignore', category=category)
    return

# version
__id__ = "$Id: WebApplication.py,v 1.3 2007-08-30 16:46:08 aivazis Exp $"

# End of file 
