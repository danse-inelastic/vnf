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


class Clerk:
    
    
    def getBvKComputation(self, id):
        from vnf.dom.BvKComputation import BvKComputation
        return self._getRecordByID(BvKComputation, id)


    def getBvKModel(self, id):
        from vnf.dom.BvKModel import BvKModel
        return self._getRecordByID(BvKModel, id)




class DeepCopier:


    def onIQEMonitor(self, iqem):
        return self._onRecordWithID( iqem )


    def onPolyXtalCoherentPhononScatteringKernel(self, kernel):
        return self._onRecordWithID( kernel )



# version
__id__ = "$Id$"

# End of file 
