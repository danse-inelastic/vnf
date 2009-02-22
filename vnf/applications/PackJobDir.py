#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2009  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.applications.Script import Script as base


class PackJobDir(base):

    class Inventory(base.Inventory):

        import pyre.inventory
        id = pyre.inventory.str('id')

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnf.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        dds = pyre.inventory.facility(name="dds", factory=vnf.components.dds)
        dds.meta['tip'] = "the component manages data files"

        csaccessor = pyre.inventory.facility(name='csaccessor', factory = vnf.components.ssher)
        csaccessor.meta['tip'] = 'computing server accessor'

        debug = pyre.inventory.bool(name='debug', default=False)
        pass # end of Inventory


    PTRFILEEXT = '.__dir__pack__ptr__'
    PACKINGINPROCESS = '***packing in process***'
    

    def main(self):
        id = self.id
        try:
            job = self.clerk.getJob(id)
        except:
            if self.debug: raise
            self._debug.log("Job %s: not found in db." % id)
            return

        server = job.server
        if not job.server:
            msg = "Job %s: server not assigned." % id
            if self.debug: raise RuntimeError, msg
            self._debug.log(msg)
            return

        if self._packingInProcess(job):
            msg = "Job %s: packing already in process." % id
            if self.debug: raise RuntimeError, msg
            self._debug.log(msg)
            return

        if self._packingIsUpToDate(job):
            msg = "Job %s: packing is already up to date." % id
            if self.debug: print msg
            self._debug.log(msg)
            return

        self._removeOldTarBall(job)
        self._declarePackingInProcess(job)

        clerk = self.clerk
        server = clerk.dereference(server)
        
        dds = self.dds
        path = dds.abspath(job, server = server)
        assert os.path.basename(path) == id

        # temporary directory
        parentdir = temproot
        parentdir = os.path.abspath(parentdir)
        tmpdirectory = tempfile.mkdtemp(dir=parentdir)
        if not os.path.exists(tmpdirectory): os.makedirs(tmpdirectory)
        subdir = os.path.basename(tmpdirectory)

        # copy job directory to the temporary dir
        csaccessor = self.csaccessor
        csaccessor.getdirectory(server, path, tmpdirectory)

        # save curdir
        curdir = os.path.abspath(os.curdir)
        # chdir to the temporary directory
        os.chdir(tmpdirectory)
        
        # create tar ball
        tarballfilename = '%s.tgz' % id
        # if file exists, remove it
        if os.path.exists(tarballfilename): os.remove(tarballfilename)

        #
        import tarfile
        tarball = tarfile.open(tarballfilename, 'w:gz')
        tarball.add(id, recursive=True)
        tarball.close()

        # remove the job directory
        shutil.rmtree(id)

        # go back to original dir
        os.chdir(curdir)
        
        # leave a pointer in the job directory
        ptr = os.path.join(subdir, tarballfilename)
        self._establishPtr(job, ptr)
        return


    def _establishPtr(self, job, ptr):
        path = self._ptrFilePath(job)
        f = open(path, 'w')
        f.write(ptr)
        return


    def _packingIsUpToDate(self, job):
        path = self._ptrFilePath(job)
        if not os.path.exists(path): return
        packtime = os.path.getmtime(path)

        server = self.clerk.dereference(job.server)
        mtime = self.dds.getmtime(job, server=server)
        return packtime > mtime
    

    def _packingInProcess(self, job):
        path = self._ptrFilePath(job)
        if not os.path.exists(path): return
        f = open(path)
        s = f.read().strip()
        return s == self.PACKINGINPROCESS


    def _removeOldTarBall(self, job):
        path = self._ptrFilePath(job)
        if not os.path.exists(path): return
        
        oldptr = open(path).read()
        oldtarballpath = os.path.join(temproot, oldptr)
        oldtarballparentdir = os.path.dirname(oldtarballpath)

        if os.path.exists(oldtarballparentdir):
            shutil.rmtree(oldtarballparentdir)
        return
    

    def _declarePackingInProcess(self, job):
        path = self._ptrFilePath(job)

        f = open(path, 'w')
        f.write(self.PACKINGINPROCESS)
        return


    def _ptrFilePath(self, job):
        return '.'.join( [self.dds.abspath(job), self.PTRFILEEXT] )


    def __init__(self, name='packjobdir'):
        super(PackJobDir, self).__init__(name)
        return


    def _configure(self):
        super(PackJobDir, self)._configure()
        self._info.log('start _configure')
        self.id = self.inventory.id

        self.debug = self.inventory.debug

        self.clerk = self.inventory.clerk
        self.clerk.director = self
        self.dds = self.inventory.dds
        self.dds.director = self
        self.csaccessor = self.inventory.csaccessor
        self._info.log('end _configure')
        return


    def _init(self):
        super(PackJobDir, self)._init()

        # initialize table registry
        import vnf.dom
        vnf.dom.register_alltables()
        return


import os, tempfile, shutil
from vnf.utils.misc import isnewer


temproot = os.path.join('..', 'content', 'data', 'tmp')



# version
__id__ = "$Id$"

# End of file 
