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
        
        from workflows.basic import login
        login(actor)

        samples_link = actor.select(type='link', label='samples')
        samples_link.click()

        new_button = actor.select(type='button', id='new-sample-button')
        new_button.click()
        
        desc_input = actor.select(type='formtextfield', name='actor.short_description')
        desc_input.type('selenium test sample')
        
        save_button = actor.select(type='formsubmitbutton', label='save')
        save_button.click()

        from workflows.basic import basic_filter
        basic_filter(actor, table='selectoneatomicstructure', key='description', value='bcc Fe*')
        
        actor.sleep(5)
        
        # !!! hack to work on table
        table = actor.selenium.lh.selector('table', id='atomicstructure-table')
        radiobutton = table + '/tbody/tr[1]/td[1]/input'
        actor.selenium.waitForElementPresent(radiobutton)
        actor.selenium.click(radiobutton)
        actor.sleep(3)
        
        select_button = actor.select(type='button', label='select')
        select_button.click()
        actor.sleep(3)

        box_button = actor.select(type='button', id='scatterer-shape-button-block')
        box_button.click()
        actor.sleep(3)

        save_button = actor.select(type='formsubmitbutton', label='Save')
        save_button.click()
        
        actor.sleep(5)
        return
        

def pysuite():
    from vnfb.testing import getDeploymentInfo
    info = getDeploymentInfo()
    fixtures = info.selenium_test_fixtures
    return makePySuite(TestCaseBase, fixtures)


def main():
    from luban.testing.selenium.Selector import debug
    debug.activate()

    pytests = pysuite()
    import unittest
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__": main()
    
# version
__id__ = "$Id$"

# End of file 
