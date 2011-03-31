#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                     California Institute of Technology
#                       (C) 2009  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from pyre.applications.Script import Script as base
"""
TODO:
    Considering that time on the remote cluster and local machine are syncronized
    is WRONG!
"""

class PackObject(base):

    class Inventory(base.Inventory):

        import pyre.inventory
        id = pyre.inventory.str('id')   # job id
        tableName = pyre.inventory.str(name='tableName', default='job')
        where = pyre.inventory.str(name='where')
        serverid = pyre.inventory.str(name='serverid')

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnf.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        dds = pyre.inventory.facility(name="dds", factory=vnf.components.dds)
        dds.meta['tip'] = "the component manages data files"

        csaccessor = pyre.inventory.facility(name='csaccessor', factory = vnf.components.ssher)
        csaccessor.meta['tip'] = 'computing server accessor'
        
        debug = pyre.inventory.bool(name='debug', default=False)

    PTRFILEEXT = '.__dir__pack__ptr__'
    PACKINGINPROCESS = '***packing in process***'
    
#    def retrieveDOMAccessor(self, name):
#        db = self.clerk.db
#        r = self.retrieveComponent(
#            name,
#            factory="accessor", args=[],
#            vault=['dom-access'])
##        if r is None:
##            curator_dump = director._dumpCurator()
##            raise RuntimeError, "could not locate dom accessor %r. curator dump: %s" % (
##                name, curator_dump)
#        r.director = self
#        return r

    def main(self):
        id = self.id
        object = self.clerk._getEntry(self.inventory.tableName, id=self.id, where=self.inventory.where)
#        try:
#            job  = self.clerk.getQEJobs(id = self.id)
#
#        except:
#            if self.debug: raise
#            self._debug.log("Job %s: not found in db." % id)
#            return

        if self._packingInProcess(object):
            msg = "Data object %s: packing already in process." % id
            if self.debug: raise RuntimeError, msg
            self._debug.log(msg)
            return

        # This method prevents from downloading results again and doesn't handle failure!
        # I'll comment out the method for further discussion
        #        if self._packingIsUpToDate(job):
        #            msg = "Job %s: packing is already up to date." % id
        #            if self.debug: print msg
        #            self._debug.log(msg)
        #            return

        self._removeOldTarBall(object)
        self._declarePackingInProcess(object)

        server  = self.clerk.getServers(id=self.inventory.serverid)

        dds = self.dds
        remotejobpath = dds.abspath(object, server = server)
        assert os.path.basename(remotejobpath) == id

        # temporary directory
        parentdir = temproot
        parentdir = os.path.abspath(parentdir)
        tmpdirectory = tempfile.mkdtemp(dir=parentdir)
        if not os.path.exists(tmpdirectory): os.makedirs(tmpdirectory)
        subdir = os.path.basename(tmpdirectory)

        # run tar cvfz at remote server
        remotejobroot = os.path.dirname(remotejobpath)
        remotejobtarball = remotejobpath + '.tgz'
        tarball = id + '.tgz'
        cmd = [
            'rm -f ' + remotejobtarball,
            ' '.join(['tar cvfz', tarball, id]),
            ]
        cmd = ';'.join(cmd)
        csaccessor = self.csaccessor
        csaccessor.execute(cmd, server, remotejobroot)
        
        # copy object tarball to the temporary dir
        csaccessor.getfile(server, remotejobtarball, tmpdirectory)

        # leave a pointer in the object directory
        ptr = os.path.join(subdir, tarball)
        self._establishPtr(object, ptr)
        return


    def _establishPtr(self, object, ptr):
        path = self._ptrFilePath(object)
        f = open(path, 'w')
        f.write(ptr)
        return


    def _packingIsUpToDate(self, object):
        path = self._ptrFilePath(object)
        if not os.path.exists(path):
            return
        packtime = os.path.getmtime(path)

        server  = self.clerk.getServers(id = self.inventory.serverid)
        mtime = self.dds.getmtime(object, server=server)
        return packtime > mtime
    

    def _packingInProcess(self, object):
        path = self._ptrFilePath(object)
        if not os.path.exists(path): return
        f = open(path)
        s = f.read().strip()
        return s == self.PACKINGINPROCESS


    def _removeOldTarBall(self, object):
        path = self._ptrFilePath(object)
        if not os.path.exists(path): return
        
        oldptr = open(path).read()
        oldtarballpath = os.path.join(temproot, oldptr)
        oldtarballparentdir = os.path.dirname(oldtarballpath)

        if os.path.exists(oldtarballparentdir):
            shutil.rmtree(oldtarballparentdir)
        return
    

    def _declarePackingInProcess(self, object):
        path = self._ptrFilePath(object)

        f = open(path, 'w')
        f.write(self.PACKINGINPROCESS)
        return


    def _ptrFilePath(self, object):
        return '.'.join( [self.dds.abspath(object), self.PTRFILEEXT] )


    def __init__(self, name='packobject'):
        super(PackObject, self).__init__(name)
        return


    def _configure(self):
        super(PackObject, self)._configure()
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
        super(PackObject, self)._init()

        # initialize table registry
        #import vnf.dom
        #vnf.dom.register_alltables()
        return


import os, tempfile, shutil
#from vnf.utils.misc import isnewer


temproot = os.path.join('..', 'content', 'data', 'tmp')



# version
__id__ = "$Id$"

# End of file 
