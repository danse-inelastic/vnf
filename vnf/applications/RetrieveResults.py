#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2008  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.applications.Script import Script as base

class RetrieveResults(base):
    
    class Inventory(base.Inventory):
        
        import pyre.inventory
        id = pyre.inventory.str('id')
        type = pyre.inventory.str('type')
        
        import pyre.idd
        idd = pyre.inventory.facility('idd-session', factory=pyre.idd.session, args=['idd-session'])
        idd.meta['tip'] = "access to the token server"

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnf.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        dds = pyre.inventory.facility(name="dds", factory=vnf.components.dds)
        dds.meta['tip'] = "the component manages data files"

        csaccessor = pyre.inventory.facility( name='csaccessor', factory = vnf.components.ssher)
        csaccessor.meta['tip'] = 'computing server accessor'

        debug = pyre.inventory.bool(name='debug', default=False)

        pass # end of Inventory
        

    def main(self):
        id = self.id
        type = self.type
        computation = self.clerk.getRecordByID(type, id)

        try:
            self.retrieve(computation)
        except Exception, e:
            self._debug.log('retrieval failed. %s: %s' % (e.__class__.__name__, e))
            import traceback
            self._debug.log(traceback.format_exc())
            d = self.dds.abspath(computation)
            try:
                import os
                if not os.path.exists(d): os.makedirs(d)
                f = self.dds.abspath(computation, 'results_retrieval_error')
                open(f, 'w').write('%s: %s' % (e.__class__.__name__, e))
            except:
                self._debug.log('failed to save error message: %s' % traceback.format_exc())
            computation.results_state = 'retrieval failed'
            self.clerk.updateRecord(computation)

            if self.debug: raise
        return


    def retrieve(self, computation):
        from vnf.components import retrieveresults
        return retrieveresults(computation, self)


    def __init__(self, name='retrieveresults'):
        base.__init__(self, name)
        return


    def _configure(self):
        base._configure(self)
        self.id = self.inventory.id
        self.type = self.inventory.type

        self.debug = self.inventory.debug

        self.idd = self.inventory.idd
        self.clerk = self.inventory.clerk
        self.clerk.director = self
        self.dds = self.inventory.dds
        self.dds.director = self
        self.csaccessor = self.inventory.csaccessor
        return


    def _init(self):
        base._init(self)

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
        return ['../content', '../config']
    


# version
__id__ = "$Id$"

# End of file 
