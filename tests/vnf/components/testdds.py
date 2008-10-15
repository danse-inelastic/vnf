#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


dataroot = 'test-dds/dataroot'


from pyre.applications.Script import Script as base

class TestApp(base):


    class Inventory(base.Inventory):

        import pyre.inventory
        import vnf.components
        
        csaccessor = pyre.inventory.facility(name='csaccessor', factory=vnf.components.ssher)
        csaccessor.meta['tip'] = 'computing server accessor'

        dds = pyre.inventory.facility(name='dds', factory=vnf.components.dds)


    def main(self, *args, **kwds):
        tmpdir = '/tmp/test-vnf-dds'
        import shutil, os
        if os.path.exists(tmpdir): shutil.rmtree(tmpdir)
        if os.path.exists(dataroot): shutil.rmtree(dataroot)
        
        dds = self.dds
        class Server: pass
        s1 = Server()
        s1.username = ''
        s1.address = 'localhost'
        s1.port = '22'
        s1.workdir = tmpdir
        dds.add_server(s1)

        if not os.path.exists(dataroot): os.makedirs(dataroot)
        open(os.path.join(dataroot,'file1'), 'w').write('hello')
        dds._remember('file1')
        dds._make_available('file1', s1)

        from vnf.dom.Job import Job
        j = Job()
        j.id = 'job000'

        jobdir = os.path.join(tmpdir, 'jobs', j.id)
        if not os.path.exists(jobdir): os.makedirs(jobdir)
        open(os.path.join(jobdir, 'calculated'), 'w').write('3.14')
        dds.remember(j, 'calculated', server=s1)

        from vnf.dom.DummyDataObject import DummyDataObject
        d = DummyDataObject()
        d.id = 'ddo000'
        dds.move(j, 'calculated', d, 'calculated', server=s1)

        dds.make_available(d)
        return


    def _configure(self):
        super(TestApp, self)._configure()
        self.csaccessor = self.inventory.csaccessor
        dds = self.inventory.dds
        dds.dataroot = dds.inventory.dataroot = dataroot
        dds.director = self
        self.dds = dds
        return


    def _init(self):
        super(TestApp, self)._init()
        return


    def _getPrivateDepositoryLocations(self):
        return ['../content', '../config']


import journal
journal.debug('curator').activate()


def main():
    app = TestApp('test')
    app.run()
    return

if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
