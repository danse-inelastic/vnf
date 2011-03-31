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


    def initSelenium(self):
        sele = super(TestCaseBase, self).initSelenium()
        sele.open(self.appaddress)
        return sele


    def test3(self):
        'vnf: bug report dialog'
        actor = self.actor

        from workflows.basic import login
        login(actor)

        l = actor.select(type='link', id='surprise-for-bug-report-test')
        l.click()

        ta = actor.select(type='formtextarea', id='bug-comment')
        ta.type('selenium test of bug report')
        actor.sleep(2)

        submit = actor.select(type='formsubmitbutton', id='bug-submit-button')
        submit.click()

        actor.sleep(3)
        
        return
    


def pysuite():
    from vnf.testing import getDeploymentInfo
    info = getDeploymentInfo()
    fixtures = info.selenium_test_fixtures
    return makePySuite(TestCaseBase, fixtures)


def main():
    from luban.testing.selenium.Selector import debug
    # debug.activate()
    
    pytests = pysuite()
    import unittest
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__": main()
    
# version
__id__ = "$Id$"

# End of file 
