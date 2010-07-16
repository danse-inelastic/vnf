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


import unittest
class TestCase(unittest.TestCase):

    def test1(self):
        from vnfb.components.Clerk import Clerk
        clerk = Clerk()
        from vnfb.deployment import dbname
        clerk.inventory.db = dbname
        clerk.importAllDataObjects()
        db = clerk.db
        tablenames = [t.getTableName() for t in db._tableregistry.itertables()]

        # check some tables
        # bvk
        self.assert_('bvkbonds' in tablenames)

        # atomic structure
        structuretable = db.getTable('atomicstructures')
        from vnfb.dom.AtomicStructure import StructureTable, AbstractOwnedObjectBase
        self.assertEqual(StructureTable, structuretable)
        AbstractOwnedObjectBase.creator
        return

    

def main():
    unittest.main()
    return



if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
