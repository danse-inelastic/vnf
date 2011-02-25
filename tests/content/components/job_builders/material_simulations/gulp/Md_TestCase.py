#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                          J Brandon Keith, Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import os


import unittest
class TestCase(unittest.TestCase):

    def test1(self):
        from memdf.gulp.Md import Md
        m = Md()
        m.xyzFile='structure.xyz'
        m.forcefield='axiallySymmetricNWS.lib'
        m.inputDeckName = ginfile = 'mMd.gin'
        m.writeInputfile()

        expected = 'expected-output'
        s = open(ginfile).read()
        s1 = open(os.path.join(expected, ginfile)).read()
        self.assertEqual(s, s1)
        return

    

def main():
    unittest.main()
    return



if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
