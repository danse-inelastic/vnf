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

from vnf.utils import atomicstructure as struct_utils

import unittest
class TestCase(unittest.TestCase):

    def test1(self):
        'makeXYZfileContent'
        from matter import Lattice, Atom, Structure
        Al = Atom('Al', (0,0,0))
        Fe = Atom('Fe', (0.5,0.5,0.5))
        atoms = [Al, Fe]
        lattice = Lattice(1,1,1, 90,90,90)
        s = Structure(atoms, lattice)
        content = struct_utils.makeXYZfileContent(s, latticeAsDescription=True)
        self.assertEqual(len(content), 4)
        self.assertEqual(int(content[0]), 2)
        self.assertEqual(len(content[1].split(' ')), 9)
        return

    

def main():
    unittest.main()
    return



if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
