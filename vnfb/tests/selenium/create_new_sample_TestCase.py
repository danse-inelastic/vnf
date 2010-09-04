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


    def test2(self):
        'vnf: bvk for bcc Fe (real user)'
        s = self.selenium
        lh = s.lh
        
        s.open(self.appaddress)

        from workflows.basic import login
        login(s)

        samples_link = 'link=samples'
        s.waitForElementPresent(samples_link)
        s.click(samples_link)

        new_link = lh.selector('div', id='new-sample-button')
        new_link += '/a'
        s.waitForElementPresent(new_link)
        s.click(new_link)

        desc_input = lh.selector('input', name='actor.short_description')
        s.waitForElementPresent(desc_input)
        s.type(desc_input, 'selenium test sample')

        save_button = lh.selector('input', type='submit', value='save')
        s.waitForElementPresent(save_button)
        s.click(save_button)

        from workflows.basic import basic_filter
        basic_filter(s, table='selectoneatomicstructure', key='description', value='bcc Fe*')
        
        lh.sleep(5)
        
        table = lh.selector('table', id='atomicstructure-table')
        radiobutton = table + '/tbody/tr[1]/td[1]/input'
        s.waitForElementPresent(radiobutton)
        s.click(radiobutton)
        lh.sleep(3)
        
        select_button = 'link=select'
        s.click(select_button)
        lh.sleep(3)

        box_button = lh.selector('div', id='scatterer-shape-button-block')
        box_button += '/a'
        s.waitForElementPresent(box_button)
        s.click(box_button)
        lh.sleep(3)

        save_button = lh.selector('input', type='submit', value='Save')
        s.waitForElementPresent(save_button)
        s.click(save_button)
        
        lh.sleep(5)
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
