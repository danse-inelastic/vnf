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


standalone = True

# application
from vnfb.testing.TestAppBase import Application as base
class TestApp(base):


    def main(self, testFacility, *args, **kwds):
        self.test1(testFacility)
        return


    def test1(self, tf):
        clerk = self.clerk
        
        db = clerk.db
        orm = clerk.orm

        # load
        # from vnfb.dom.Atom import Atom
        # atom = orm.load(Atom, '3BEYWG5W')

        # save matter
        from vnfb.dom.AtomicStructure import Structure
        matter = Structure()
        matter.short_description = 'test structure'
        orm.save(matter)

        return



import unittest
class TestCase(unittest.TestCase):

    def test(self):
        app = TestApp('main')
        app.run(self)
        return
    
        
def main():
    unittest.main()
    return



if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
