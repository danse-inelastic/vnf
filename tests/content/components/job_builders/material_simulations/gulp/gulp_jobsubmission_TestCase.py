'''
Test of component job_builders/material_simulations/gulp/optimization.odb

Test assumes that
 1. database. see parameter "dbname"
 2. there is a bvk_getphonons record and a job record for that computation

'''


# id for computation record.
recordid = "3ZNHWIM6" 


# application
from vnf.testing.job_builder import TestApp as base
class TestApp(base):


    def main(self, testFacility):
        domaccess = self.retrieveDOMAccessor('material_simulations/gulpSettings')
        computation = domaccess.getComputationRecord('phonons', recordid)
        return base.main(self, computation, testFacility)


    def _checkJobDir(self):
        return

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
