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
Test of component job_builders/material_simulations/phonon_calculators/bvk_getphonons

Test assumes that
 1. database. see parameter "dbname"
 2. there is a bvk_getphonons record and a job record for that computation

'''


# id for computation record.
recordid = "fortest" 


# application
from vnfb.testing.job_builder import TestApp as base
class TestApp(base):


    def main(self, testFacility):
        domaccess = self.retrieveDOMAccessor('material_simulations/phonon_calculators/bvk')
        computation = domaccess.getComputationRecord('phonons', recordid)
        return base.main(self, computation, testFacility)


    def _checkJobDir(self):
        return
        
        

import os


import unittest
class TestCase(unittest.TestCase):

    def test1(self):
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
