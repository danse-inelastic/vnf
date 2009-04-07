#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from vnf.utils.misc import isnewer
import tempfile, os, shutil


import unittest

from unittest import TestCase
class TestCase(TestCase):


    def test1(self):
        'isnewer: file'
        f = tempfile.mktemp()
        open(f, 'w').write('')
        t = os.path.getmtime(f)

        self.assert_(isnewer(f, t))
        self.assert_(not isnewer(f, t+1))

        os.remove(f)
        return
    
    
    def test2(self):
        'isnewer: dir'
        d = tempfile.mkdtemp()
        t = os.path.getmtime(d)

        self.assert_(isnewer(d, t))
        self.assert_(not isnewer(d, t+0.01))

        import time
        time.sleep(1)

        f1 = os.path.join(d, 'f1')
        open(f1,'w').write('')

        self.assert_(isnewer(d, t+0.01))

        t = os.path.getmtime(f1)
        
        time.sleep(1)
        open(f1, 'w').write('')
        self.assert_(isnewer(d, t+0.01))

        shutil.rmtree(d)
        return
    
    
    pass # end of TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
