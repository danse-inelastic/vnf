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


    def test2(self):
        'vnf: bvk for bcc Fe (real user)'
        from realuser import username, password
        
        s = self.selenium
        lh = s.lh
        
        s.open(self.appaddress)

        from workflows.basic import login, basic_filter
        login(s, username=username, password=password)

        basic_filter(s, table='atomicstructure', key='description', value='bcc Fe*')
        lh.sleep(5)

        table = lh.selector('table', id='atomicstructure-table')
        structlink = table + '/tbody/tr[1]/td[2]/a'
        s.waitForElementPresent(structlink)
        s.click(structlink)

        lh.expandDocument(id = 'atomicstructure-computed-phonons')

        startnew_link = lh.selector('a', id='start-new-phonon-computation-link')
        s.waitForElementPresent(startnew_link)
        s.click(startnew_link)

        bvk_radiobutton = lh.selector('input', type='radio', value='bvk')
        s.waitForElementPresent(bvk_radiobutton)
        s.click(bvk_radiobutton)

        submit_button = lh.selector('div', id='phonons-select-engine-submit-button')
        submit_button += '/input'
        s.waitForElementPresent(submit_button)
        s.click(submit_button)

        selectmodel_link = 'link=select this model'
        s.waitForElementPresent(selectmodel_link)
        s.click(selectmodel_link)
        
        dos_radiobutton = lh.selector('input', type='radio', value='dos')
        s.waitForElementPresent(dos_radiobutton)
        s.click(dos_radiobutton)

        submit_button = lh.selector('div', id='bvk-select-target-submit-button')
        submit_button += '/input'
        s.waitForElementPresent(submit_button)
        s.click(submit_button)

        save_button = lh.selector('input', type='submit', value='Save')
        s.waitForElementPresent(save_button)
        s.click(save_button)

        submitjob_button = lh.selector('input', type='submit', value='submit')
        s.waitForElementPresent(submitjob_button)
        s.click(submitjob_button)

        lh.sleep(5)
        switch_link = lh.selector('div', id='job-switch-to-computation-link')
        switch_link += '/a'
        s.waitForElementPresent(switch_link)
        s.click(switch_link)

        lh.expandDocument(id='bvk_getdos-view-results-doc')

        # temporary disable the following
        #
        return
        resultsdoc_div = lh.selector('div', id='bvk_getdos-view-results-doc')
        hist_expandctrl = resultsdoc_div + '/div[2]/div[1]/div[1]/div[1]/div[1]/table/tbody/tr/td[1]/a'
        s.waitForElementPresent(hist_expandctrl)
        s.click(hist_expandctrl)
        
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
