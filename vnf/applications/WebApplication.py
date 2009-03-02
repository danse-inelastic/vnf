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

        from vnf.components import clerk
        clerk = pyre.inventory.facility(name="clerk", factory=clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        from vnf.components import dds
        dds = pyre.inventory.facility(name="dds", factory=dds)
        dds.meta['tip'] = "the component manages data files"

        from vnf.components import scribe
        scribe = pyre.inventory.facility(name="scribe", factory=scribe)
        scribe.meta['tip'] = "the component responsible for rendering the generated reports"

        from vnf.components import ssher
        csaccessor = pyre.inventory.facility( name='csaccessor', factory = ssher)
        csaccessor.meta['tip'] = 'computing server accessor'

        debug = pyre.inventory.bool(name="debug", default=True)
        debug.meta['tip'] = "suppress some html output for debugging purposes"

        imagepath = pyre.inventory.str(name='imagepath', default = '/vnf/images' )
        javascriptpath = pyre.inventory.str(name='javascriptpath', default = '/vnf/javascripts' )
        javapath = pyre.inventory.str(name='javapath', default = '/vnf/java' )
        tmproot = pyre.inventory.str(name='tmproot', default = '/vnf/tmp')
        

    def main(self, *args, **kwds):

        actor = self.actor
        if actor is None:
            inquiry = self.inventory._getTraitDescriptor('actor').inquiry
            actor = self.retrieveActor('nyi')
            actor.message = "Not implemented yet! actor=%s, routine=%s" % (
                inquiry, self.inventory.routine)
            self.actor = actor

        noErrors=True
        try:
            page = self.actor.perform(self, routine=self.inventory.routine, debug=self.debug)
            if isinstance(page, basestring):
                print page,
            else:
                self.render(page)
        except:
            noErrors=False
            bugid, errmsg = self.generateDebugInfo()
            self.redirect(actor='bug-report', routine='default', bugid = bugid, traceback = errmsg)
            
        if noErrors and self.debug:
            self.generateDebugInfo('generic')
        return
    
    def generateDebugInfo(self,filetypes='unique'):
        if filetypes is 'unique':
            #from vnf.dom.idgenerator import idFromTime as idgenerator
            from vnf.dom.idgenerator import generator as idgenerator
            id = idgenerator()
            self._debug.log('*** Error: %s' % id)
        else:
            id = 'debugInfo'

        import os
        logroot = '../log'
        
        from configurationSaver import toPml
        pmlpath = os.path.join(logroot, id + '.pml')
        toPml(self, pmlpath)

        errorspath = os.path.join(logroot, id + '.errors')
        import traceback
        errmsg = traceback.format_exc()
        open(errorspath, 'w').write(errmsg)

        inputspath = os.path.join(logroot, id + '.inputs')
        text = ['%s=%s' % (k,v) for k,v in self._cgi_inputs.iteritems()]
        text = '\n'.join(text)
        open(inputspath, 'w').write(text)

        return id, errmsg
            

    
    def _oldmain(self, *args, **kwds):
        if self.debug:
            from configurationSaver import toPml
            from os import environ
            user = environ.get('USER') or 'webserver'
            toPml(self, '/tmp/main-debug-%s.pml' % user)
#            if user is 'jbk' or environ:
#                import traceback
#                out = open( '../log/vnf-error-%s.log' % user, 'w' )
#                out.write( traceback.format_exc() )
#                toPml(self, '../config/main.pml')
        actor = self.actor
        if actor is None:
            inquiry = self.inventory._getTraitDescriptor('actor').inquiry
            actor = self.retrieveActor('nyi')
            actor.message = "Not implemented yet! actor=%s, routine=%s" % (
                inquiry, self.inventory.routine)
            self.actor = actor
            
        page = self.actor.perform(self, routine=self.inventory.routine, debug=self.debug)
        self.render(page)
        return


    def redirect(self, actor, routine, **kwds):
        self.inventory.routine = routine
        self.actor = self.retrieveActor(actor)
        
        if self.actor is not None:
            self.configureComponent(self.actor)
            for k,v in kwds.iteritems():
                setattr(self.actor.inventory, k, v)

        try:
            self.main()
        except:
            raise RuntimeError, "redirect to actor %r, routine %r, with kwds %r failed" % (
                actor, routine, kwds)
        return


    def retrievePage(self, name):
        page = super(WebApplication, self).retrievePage(name)
        if page:
            return page

        if self.debug:
            self._debug.log( "*** could not locate page %r" % name )
            page = super(WebApplication, self).retrievePage("page-loading-error")
            return page
        
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

        from vnf.components import accesscontrol
        self.accesscontrol = accesscontrol()

        import os
        configurations = {
            'home': self.home,
            'cgihome':self.cgihome,
            'imagepath':self.inventory.imagepath,
            'javascriptpath':self.inventory.javascriptpath,
            'javapath':self.inventory.javapath,
            'tmproot': self.inventory.tmproot,
            }
        import vnf.weaver
        vnf.weaver.extend_weaver(self.pageMill, configurations )

        if not self.debug: suppressWarnings()
        return


    def _init(self):
        super(WebApplication, self)._init()

        # accesscontrol need to know the database
        self.accesscontrol.db = self.clerk.db
        
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
        content = join(root, 'content')
        config = join(root, 'config')
        
        from vnf.depositories import depositories

        return depositories(content)+[config]
        


def suppressWarnings():
    import warnings
    categories_to_ignore = [
        DeprecationWarning,
        ]
    for category in categories_to_ignore:
        warnings.filterwarnings('ignore', category=category)
    return


import journal
journal.error('pyre.inventory').deactivate()
    

if __name__=='__main__':
    w=WebApplication(name='test')
    print w

# version
__id__ = "$Id: WebApplication.py,v 1.3 2007-08-30 16:46:08 aivazis Exp $"

# End of file 
