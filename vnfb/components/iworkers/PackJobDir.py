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


from pyre.components.Component import Component as base


class PackJobDir(base):

    class Inventory(base.Inventory):

        pass # end of Inventory


    def run(self, task):
        director = self.director

        #
        domaccess = self.domaccess = director.retrieveDOMAccessor('job')
        # make sure orm is initd
        orm = domaccess.orm
        # db manager
        db = domaccess.db

        director.declareProgress(0.1, 'Verifying job ...')
        job = task.beneficiary.dereference(db)
        id = job.id

        # check job status
        state = job.state
        if state not in ['finished', 'terminated', 'running']:
            raise RuntimeError, "Job %s not suitable for packing: %s" % (id, state)
        
        # check there is server
        server = job.server
        if not job.server:
            msg = "Job %s: server not assigned." % id
            self._debug.log(msg)
            return

##         if self._packingInProcess(job):
##             msg = "Job %s: packing already in process." % id
##             if self.debug: raise RuntimeError, msg
##             self._debug.log(msg)
##             return

##         if self._packingIsUpToDate(job):
##             msg = "Job %s: packing is already up to date." % id
##             if self.debug: print msg
##             self._debug.log(msg)
##             return

        director.declareProgress(0.2, 'Removing old tar ball if necessary ...')
        packjobdir.removeOldTarBall(job, director)
        packjobdir.declarePackingInProcess(job, director)

        server = domaccess.db.dereference(server)
        
        dds = director.dds
        remotejobpath = dds.abspath(job, server = server)
        assert os.path.basename(remotejobpath) == id
        
        # temporary directory
        director.declareProgress(0.3, 'Creating a temporary directory locally to store the tar ball ...')
        parentdir = packjobdir.temproot
        parentdir = os.path.abspath(parentdir)
        tmpdirectory = tempfile.mkdtemp(dir=parentdir)
        if not os.path.exists(tmpdirectory): os.makedirs(tmpdirectory)
        subdir = os.path.basename(tmpdirectory)

        # run tar cvfz at remote server
        director.declareProgress(0.4, 'Packing in the remote server ...')
        remotejobroot = os.path.dirname(remotejobpath)
        remotejobtarball = remotejobpath + '.tgz'
        tarball = id + '.tgz'
        cmd = [
            'rm -f ' + remotejobtarball,
            ' '.join(['tar cvfz', tarball, id]),
            ]
        cmd = ';'.join(cmd)
        csaccessor = director.csaccessor
        csaccessor.execute(cmd, server, remotejobroot)
        
        # copy job tarball to the temporary dir
        director.declareProgress(0.7, 'Copying tarball to vnf server ...')
        csaccessor.getfile(server, remotejobtarball, tmpdirectory)

        # leave a pointer in the job directory
        ptr = os.path.join(subdir, tarball)
        packjobdir.establishPtr(job, ptr, director)

        director.declareProgress(1, 'Done ...')
        return



import os, tempfile, shutil
from vnfb.utils.job import packjobdir



# version
__id__ = "$Id$"

# End of file 
