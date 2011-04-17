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
        'vnf: bvk for bcc Fe (demo user)'
        actor = self.actor
        
        from workflows.basic import login, basic_filter
        login(actor)
        
        basic_filter(actor, table='atomicstructure', key='description', value='bcc Fe*')
        actor.sleep(4)
        
        # !!! 
        # hack
        table = actor.selenium.lh.selector('table', id='atomicstructure-table')
        structlink = table + '/tbody/tr[1]/td[3]/a'
        actor.selenium.waitForElementPresent(structlink)
        actor.selenium.click(structlink)
        
        doc = actor.select(type='document', id = 'atomicstructure-computed-phonons')
        doc.expand()
        
        startnew_link = actor.select(type='link', id='start-new-phonon-computation-link')
        startnew_link.click()
        
        actor.sleep(4)
        self.assert_(actor.getAlert())
        
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
