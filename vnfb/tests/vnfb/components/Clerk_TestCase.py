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
        #self.test1(testFacility)
        self.test2(testFacility)
        return


    def test2(self, tf):
        clerk = self.clerk
        
        # clerk.importAllDataObjects()
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

        # save scatterer
        from vnfb.dom.neutron_experiment_simulations.Scatterer import Scatterer
        scatterer = Scatterer()
        scatterer.short_description = 'test'
        scatterer.matter = matter
        orm = clerk.orm
        orm.save(scatterer, save_not_owned_referred_object=False)
        return
    

    def test1(self, tf):
        clerk = self.clerk
        clerk.importAllDataObjects()
        db = clerk.db
        tablenames = [t.getTableName() for t in db._tableregistry.itertables()]

        # check some tables
        # bvk
        tf.assert_('bvkbonds' in tablenames)

        # atomic structure
        structuretable = db.getTable('atomicstructures')
        from vnfb.dom.AtomicStructure import StructureTable, AbstractOwnedObjectBase
        tf.assertEqual(StructureTable, structuretable)
        AbstractOwnedObjectBase.creator
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
