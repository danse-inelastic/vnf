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


'''
Test of component job_builders/neutronexperiment.odb

Test assumes that
 1. database. see parameter "dbname"
 2. there is a neutronexperiment db record (with all the necessary associated records)
 3. there is a job db record for the neutronexperiment record

'''


standalone = True


from vnfb.testing.job_builder import TestApp as base


class TestApp(base):


    def main(self, expid, testFacility):
        domaccess = self.retrieveDOMAccessor('experiment')
        computation = domaccess.getExperimentRecord(expid)
        return base.main(self, computation, testFacility)


    def _checkJobDir(self):
        return


import unittest
class TestCase(unittest.TestCase):

    def test1(self):
        app = TestApp('main')
        app.run('test-arcs-detector-system', self)
        return

    

def main():
    unittest.main()
    return



if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
