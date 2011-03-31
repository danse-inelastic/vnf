from selenium import selenium
import unittest, time, re

class NewTest(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://change-this-to-the-site-you-are-testing/")
        self.selenium.start()
    
    def test_new(self):
        sel = self.selenium
        sel.open("/vnf/alpha/cgi-bin/main.cgi?sentry.ticket=jbrkeith99ae57800b4d54d81410e9df3759c3db&sentry.username=jbrkeith&actor=greet")
        sel.click("link=Samples")
        sel.wait_for_page_to_load("30000")
        sel.click("//div[@id='portlet-main--tree']/div/div[3]/a/span")
        sel.wait_for_page_to_load("30000")
        sel.type("text1", "polycrystalline")
        sel.click("submit")
        sel.wait_for_page_to_load("30000")
        sel.click("submit")
        sel.wait_for_page_to_load("30000")
        sel.type("text1", "chromium")
        sel.type("ax", "2.88")
        sel.type("by", "2.88")
        sel.type("cz", "2.88")
        sel.type("listOfAtoms", "Cr 0.0 0.0 0.0\nCr 0.5 0.5 0.5")
        sel.click("submit")
        sel.wait_for_page_to_load("30000")
        sel.click("radio1")
        sel.click("submit")
        sel.wait_for_page_to_load("30000")
        sel.click("submit")
        sel.wait_for_page_to_load("30000")
        sel.click("//div[@id='portlet-main--tree']/div/div[1]/a/span")
        sel.wait_for_page_to_load("30000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
