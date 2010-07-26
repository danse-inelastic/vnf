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


from luban.testing.selenium.TestCaseBase import TestCaseBase as base, makePySuite

class TestCaseBase(base):

    targetapp = 'vnf'


    def test1(self):
        'vnf: login'
        s = self.selenium

        s.open(self.appaddress)

        username = "//div[@id='login-username-input']"
        password = "//div[@id='login-password-input']"
        inputsubelem = '/table/tbody/tr/td[1]/input'
        s.waitForElementPresent(username)
        s.type(username+inputsubelem, 'demo')
        s.type(password+inputsubelem, 'demo')

        submit = "//input[@type='submit']"
        s.click(submit)

        minimize = "//div[@id='minimize-help-button']/a/span"
        s.waitForElementPresent(minimize)
        s.click(minimize)

        select = s.lh.formfield('atomicstructure-table-basic-filter-key', 'select')
        s.select(select, 'description')
        s.type(s.lh.formfield('atomicstructure-table-basic-filter-value', 'input'),
               'bcc Fe*')
        
        s.lh.sleep(2)
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
