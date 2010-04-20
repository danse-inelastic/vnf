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


from luban.applications.UIApp import Extension as Base
class AppExtension(Base):


    class Inventory(Base.Inventory):
        
        import pyre.inventory

        import vnfb.components
        dds = pyre.inventory.facility(name="dds", factory=vnfb.components.dds)
        dds.meta['tip'] = "the component manages data files"

        csaccessor = pyre.inventory.facility( name='csaccessor', factory = vnfb.components.ssher)
        csaccessor.meta['tip'] = 'computing server accessor'
        
        itaskmanager = pyre.inventory.facility(name='itaskmanager', default = 'itask-manager')


    def retrieveDOMAccessor(self, name):
        director = self.director
        db = director.clerk.db
        r = director.retrieveComponent(
            name,
            factory="accessor", args=[],
            vault=['dom-access'])
        if r is None:
            curator_dump = director._dumpCurator()
            raise RuntimeError, "could not locate dom accessor %r. curator dump: %s" % (
                name, curator_dump)
        r.director = director
        return r

    
    def _configure(self):
        super(AppExtension, self)._configure()

        self.dds = self.inventory.dds
        self.csaccessor = self.inventory.csaccessor
        self.itaskmanager = self.inventory.itaskmanager

        from vnfb.components import accesscontrol
        self.accesscontrol = accesscontrol()

        return
    

    def _init(self):
        super(AppExtension, self)._init()

        director = self.director
        
        # transfer to director
        # is this really the good thing to do?
        director.dds = self.dds
        director.csaccessor = self.csaccessor
        director.itaskmanager = self.itaskmanager
        director.accesscontrol = self.accesscontrol
        self.dds.director = director

        director.retrieveDOMAccessor = self.retrieveDOMAccessor
        
        # accesscontrol need to know the database
        self.accesscontrol.clerk = director.clerk
        self.accesscontrol.sentry = director.sentry
        return



# version
__id__ = "$Id$"

# End of file 
