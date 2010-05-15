#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from vnfb.utils.material_simulations.bvkutils import findForceContantTensorConstraints


import unittest
class TestCase(unittest.TestCase):

    def test1(self):
        # simple cubic
        import matter
        lattice = matter.Lattice(a=1, b=1, c=1, alpha=90, beta=90, gamma=90)
        struct = matter.Structure([matter.Atom('H')], lattice=lattice, sgid=221)

        from bvk.BvKBond import BvKBond
        bond = BvKBond()
        bond.matter = struct
        bond.uses_primitive_unitcell = 1
        bond.A = 0
        bond.B = 0
        bond.Boffset = [1,1,0]
        bond.Boffset_is_fractional = 0
        
        # 110
        print 'bond 110 for sc lattice'
        for constraint in  findForceContantTensorConstraints(bond):
            print constraint
            
        return


    def test2(self):
        # simple cubic
        import matter
        lattice = matter.Lattice(a=1, b=1, c=1, alpha=90, beta=90, gamma=90)
        atom1 = matter.Atom('C')
        atom2 = matter.Atom('H', [0.5, 0.5, 0])
        atom3 = matter.Atom('H', [0.5, 0, 0.5])
        atom4 = matter.Atom('H', [0, 0.5, 0.5])
        struct = matter.Structure([atom1, atom2, atom3, atom4], lattice=lattice, sgid=221)

        from bvk.BvKBond import BvKBond
        bond = BvKBond()
        bond.matter = struct
        bond.uses_primitive_unitcell = 1
        bond.A = 0
        bond.B = 0
        bond.Boffset = [1,1,0]
        bond.Boffset_is_fractional = 0
        
        # 110
        print 'bond 110 for sc lattice'
        for constraint in  findForceContantTensorConstraints(bond):
            print constraint
            
        return


    def test3(self):
        # simple cubic
        import matter
        lattice = matter.Lattice(a=3.701, b=3.701, c=3.701, alpha=90, beta=90, gamma=90)
        atom1 = matter.Atom('C')
        atom2 = matter.Atom('H', [0.5, 0.5, 0])
        atom3 = matter.Atom('H', [0.5, 0, 0.5])
        atom4 = matter.Atom('H', [0, 0.5, 0.5])
        struct = matter.Structure([atom1, atom2, atom3, atom4], lattice=lattice, sgid=221)

        from bvk.BvKBond import BvKBond
        bond = BvKBond()
        bond.matter = struct
        bond.uses_primitive_unitcell = 1
        bond.A = 0
        bond.B = 0
        bond.Boffset = [1,1,0]
        bond.Boffset_is_fractional = 0
        
        # 110
        print 'bond 110 for sc lattice'
        for constraint in  findForceContantTensorConstraints(bond):
            print constraint
            
        return


    def test3a(self):
        # simple cubic
        import matter
        lattice = matter.Lattice(a=3.701, b=3.701, c=3.701, alpha=90, beta=90, gamma=90)
        atom1 = matter.Atom('C')
        atom2 = matter.Atom('H', [0.5, 0.5, 0])
        atom3 = matter.Atom('H', [0.5, 0, 0.5])
        atom4 = matter.Atom('H', [0, 0.5, 0.5])
        struct = matter.Structure([atom1, atom2, atom3, atom4], lattice=lattice, sgid=221)

        from bvk.BvKBond import BvKBond
        bond = BvKBond()
        bond.matter = struct
        bond.uses_primitive_unitcell = 1
        bond.A = 0
        bond.B = 1
        bond.Boffset = [0,0.5,0.5]
        bond.Boffset_is_fractional = 1
        
        # 110
        print 'bond 00.50.5 for sc lattice'
        for constraint in  findForceContantTensorConstraints(bond):
            print constraint
            
        return


def main():
    unittest.main()
    return

if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
