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


    def test3(self):
        'vnf: bug report dialog'
        s = self.selenium
        
        s.open(self.appaddress)

        from workflows.basic import login
        login(s)

        link = s.lh.selector(tag='a', id='surprise-for-bug-report-test')
        print link
        s.waitForElementPresent(link)
        s.click(link)

        ta = s.lh.formfield(id='bug-comment', type='textarea')
        s.waitForElementPresent(ta)
        s.type(ta, 'selenium test of bug report')

        
        submit = s.lh.selector(tag='input', type='submit', name='actor.bug-submit')
        s.click(submit)
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
