#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

# skip = True

from luban.testing.selenium.TestCaseBase import TestCaseBase as base, makePySuite

class TestCaseBase(base):

    targetapp = 'vnf'


    def initSelenium(self):
        sele = super(TestCaseBase, self).initSelenium()
        sele.open(self.appaddress)
        return sele


    def test1(self):
        'vnf: login'
        from workflows.basic import login
        login(self.actor)
        return


    def test2(self):
        'vnf: filter by description to find bcc Fe*'

        actor = self.actor

        from workflows.basic import login, basic_filter
        login(actor)
        basic_filter(
            actor, 
            table='atomicstructure', 
            key='description', 
            value='bcc Fe*',
            )

        actor.sleep(3)
        return



def pysuite():
    from vnf.testing import getDeploymentInfo
    info = getDeploymentInfo()
    fixtures = info.selenium_test_fixtures
    return makePySuite(TestCaseBase, fixtures)


def main():
    pytests = pysuite()
    import unittest
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__": main()
    
# version
__id__ = "$Id$"

# End of file 
