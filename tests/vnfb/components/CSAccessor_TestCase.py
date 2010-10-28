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
skip = True


import os

# application
from vnfb.testing.TestAppBase import Application as base
class TestApp(base):

    
    class Inventory(base.Inventory):

        import pyre.inventory
        server1 = pyre.inventory.str('server1', default='danse-vnf-admin@localhost(50022)')
        server2 = pyre.inventory.str('server2', default='danse-vnf-admin@foxtrot.danse.us')


    def main(self, testFacility, *args, **kwds):
        # self.test1(testFacility)
        self.test2(testFacility)
        return


    def test1(self, tf):
        'copyfile: local->remote'
        csaccessor = self.csaccessor
        server1 = self.server1
        server2 = self.server2
        localhost = self.localhost
        
        src = os.path.abspath('a.txt')
        dest = '/tmp/a.txt'
        
        #
        csaccessor.copyfile(localhost, src, server2, dest)
        #
        self._checkfile(server2, dest, 'a'*50, tf)
        return


    def test2(self, tf):
        'copyfile: remote->remote'
        csaccessor = self.csaccessor
        server1 = self.server1
        server2 = self.server2
        localhost = self.localhost
        
        # copy to server1
        path1 = '/tmp/vnf-test-csaccessor'
        csaccessor.execute('mkdir -p %s' % path1, server1, '')
        csaccessor.pushdir('data', server1, path1)

        # *** server1/dir -> server2/dir, no tunneling 
        # clean up server2
        csaccessor.execute('rm -rf %s' % path1, server2, '')

        # copy from server1 to server2
        csaccessor.copyfile(server1, path1, server2, path1)
        
        # check
        file1 = os.path.join(path1, 'data', 'a.txt')
        self._checkfile(server2, file1, 'a'*50, tf)

        # *** server1/file -> server2/file, no tunneling 
        # clean up server2
        csaccessor.execute('rm -rf %s' % file1, server2, '')

        # copy from server1 to server2
        csaccessor.copyfile(server1, file1, server2, file1)
        
        # check
        self._checkfile(server2, file1, 'a'*50, tf)

        # *** server1 -> server1
        # clean up server1, place b
        path1b = '/tmp/vnf-test-csaccessor-b'
        csaccessor.execute('rm -rf %s' % path1b, server1, '')
        csaccessor.copyfile(server1, path1, server1, path1b)
        file1b = os.path.join(path1b, 'data', 'a.txt')
        self._checkfile(server1, file1b, 'a'*50, tf)
        
        return

    
    def _checkfile(self, server, path, content, tf):
        csaccessor = self.csaccessor
        failed, out, err = csaccessor.execute(
            'test -f %s; echo $?' % path, server, '')
        tf.assert_(not failed)
        tf.assertEqual(int(out), 0)
        failed, out, err = csaccessor.execute(
            'cat %s' % path, server, '')
        tf.assert_(not failed)
        tf.assertEqual(out.strip(), content)
        return
    

    def _configure(self):
        super(TestApp, self)._configure()
        self.server1 = self._decode(self.inventory.server1)
        self.server2 = self._decode(self.inventory.server2)
        self.localhost = self._decode('localhost')
        return


    def _decode(self, url):
        from vnfb.components.DistributedDataStorage import _decodesurl
        return _decodesurl(url)


import unittest
class TestCase(unittest.TestCase):

    def test(self):
        app = TestApp('main')
        app.run(self)
        return
    
        
import unittest
def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )


def main():
    import journal
    pytests = pysuite()
    unittest.TextTestRunner(verbosity=2).run(pytests)
    return


if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
