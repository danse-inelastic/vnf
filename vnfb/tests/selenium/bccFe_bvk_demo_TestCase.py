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

skip = True

from luban.testing.selenium.TestCaseBase import TestCaseBase as base, makePySuite

class TestCaseBase(base):

    targetapp = 'vnf'


    def test1(self):
        'vnf: bvk for bcc Fe (demo user)'
        s = self.selenium
        lh = s.lh
        
        s.open(self.appaddress)
        
        from workflows.basic import login, basic_filter
        login(s)
        
        basic_filter(s, table='atomicstructure', key='description', value='bcc Fe*')
        lh.sleep(4)
        
        table = lh.selector('table', id='atomicstructure-table')
        structlink = table + '/tbody/tr[1]/td[2]/a'
        s.waitForElementPresent(structlink)
        s.click(structlink)
        
        lh.expandDocument(id = 'atomicstructure-computed-phonons')
        
        startnew_link = lh.selector('a', id='start-new-phonon-computation-link')
        s.waitForElementPresent(startnew_link)
        s.click(startnew_link)
        
        lh.sleep(4)
        self.assert_(s.get_alert())
        
        return
        

def pysuite():
    from vnfb.testing import getDeploymentInfo
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
