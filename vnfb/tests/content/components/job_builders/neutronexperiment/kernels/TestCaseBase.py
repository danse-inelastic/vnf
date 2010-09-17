#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from TestAppBase import TestAppBase

def createTestCase(App):
    import unittest
    class TestCase(unittest.TestCase):

        def test1(self):
            name = 'main'
            app = App(name)
            app.run(self)
            return

    return TestCase


# version
__id__ = "$Id$"

# End of file 
