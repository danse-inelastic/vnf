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


from TestCaseBase import createTestCase, TestAppBase

class TestApp(TestAppBase):
    
    from vnfb.dom.scattering_kernels.ins.PolyXtalCoherentPhononScatteringKernel import PolyXtalCoherentPhononScatteringKernel as Kernel

    def getKernel(self):
        orm = self.clerk.orm
        return orm.load(self.Kernel, id='bvk-bccFeAt295-N40-df0.2-example1')


TestCase = createTestCase(TestApp)


def main():
    import unittest
    unittest.main()
    return

if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
