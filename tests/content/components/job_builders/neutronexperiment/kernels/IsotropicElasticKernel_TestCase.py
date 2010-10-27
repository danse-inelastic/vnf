#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


standalone = True


from TestCaseBase import createTestCase, TestAppBase

class TestApp(TestAppBase):
    
    
    from vnfb.dom.scattering_kernels.IsotropicElasticKernel import IsotropicElasticKernel as Kernel
    
    
    kernelid = 'testjobbuilder'
    def getKernel(self):
        orm = self.clerk.orm
        db = orm.db
        KernelTable = orm(self.Kernel)
        ks = db.query(KernelTable).filter_by(id=self.kernelid).all()
        if not ks:
            return self.createKernel()
        return orm.record2object(ks[0])
    
    
    def createKernel(self):
        orm = self.clerk.orm
        db = orm.db
        KernelTable = orm(self.Kernel)
        r = KernelTable()
        r.id = self.kernelid
        db.insertRow(r)
        return orm.record2object(r)


TestCase = createTestCase(TestApp)


import unittest
def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )


def main():
    import journal
    pytests = pysuite()
    unittest.TextTestRunner(verbosity=2).run(pytests)
    return

if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
