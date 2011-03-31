#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import unittest
import math

class TestNodes(unittest.TestCase):
    
    def setUp(self):
        self.proclist   = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24, 36, 48, 60, 72)   # Number of cores
        self.expected   = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6)
        self.procPerNode = 12
    
    def testGetNodes(self):
        "Calculates number of nodes (nodes) from number of processors"
        for i in range(len(self.proclist)):
            numnodes    = int(math.ceil(self.proclist[i]/float(self.procPerNode)))
            self.assertEqual(self.expected[i], numnodes)

if __name__ == '__main__':
    unittest.main()


__date__ = "$Mar 3, 2010 4:02:02 PM$"


