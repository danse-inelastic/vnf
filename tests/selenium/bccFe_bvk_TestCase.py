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


    def test2(self):
        'vnf: bvk for bcc Fe (real user)'
        
        actor = self.actor 
        
        from realuser import username, password
        
        from workflows.basic import login, basic_filter
        login(actor, username=username, password=password)

        basic_filter(actor, table='atomicstructure', key='description', value='bcc Fe*')
        actor.sleep(5)

        # !!!
        # hack
        table = actor.selenium.lh.selector('table', id='atomicstructure-table')
        structlink = table + '/tbody/tr[1]/td[3]/a'
        actor.selenium.waitForElementPresent(structlink)
        actor.selenium.click(structlink)

        actor.select(type='document', id = 'atomicstructure-computed-phonons').expand()

        startnew_link = actor.select(type='link', id='start-new-phonon-computation-link')
        startnew_link.click()

        engineradiobox = actor.select(type='formradiobox', name='engine')
        engineradiobox.select('bvk')

        submit_button = actor.select(
            type='formsubmitbutton', 
            id='phonons-select-engine-submit-button',
            )
        submit_button.click()

        selectmodel_link = actor.select(type='link', label='select this model')
        selectmodel_link.click()
        
        targetradiobox = actor.select(type='formradiobox', name='target')
        targetradiobox.select('dos')

        submit_button = actor.select(
            type='formsubmitbutton', 
            id='bvk-select-target-submit-button',
            )
        submit_button.click()

        save_button = actor.select(
            type = 'formsubmitbutton',
            label = 'Save',
            )
        save_button.click()

        submitjob_button = actor.select(
            type = 'formsubmitbutton',
            label = 'submit',
            )
        submitjob_button.click()

        actor.sleep(5)
        switch_link = actor.select(
            type = 'button',
            id='job-switch-to-computation-link',
            )
        switch_link.click()
        
        doc = actor.select(type='document', id='bvk_getdos-view-results-doc')
        doc.expand()
        
        # temporary disable the following
        #
        return
        resultsdoc = actor.select(
            type='document', 
            id='bvk_getdos-view-results-doc',
            )
        resultsdoc.expand()
        
        lh.sleep(5)
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
