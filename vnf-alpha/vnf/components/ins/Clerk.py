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
        from vnf.dom.ins.BvKComputation import BvKComputation
        return self._getRecordByID(BvKComputation, id)


    def getBvKModel(self, id):
        from vnf.dom.ins.BvKModel import BvKModel
        return self._getRecordByID(BvKModel, id)


    def getQEComputation(self, id):
        from vnf.dom.ins.QEComputation import QEComputation
        return self._getRecordByID(QEComputation, id)



class DeepCopier:


    def onIQEMonitor(self, iqem):
        return self._onRecordWithID( iqem )


    def onPolyXtalCoherentPhononScatteringKernel(self, kernel):
        return self._onRecordWithID( kernel )


    def onSQEKernel(self, kernel):
        return self._onRecordWithID( kernel )


# version
__id__ = "$Id$"

# End of file 
