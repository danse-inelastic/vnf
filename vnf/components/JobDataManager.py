# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import journal
debug = journal.debug('job')


class JobDataManager:

    '''manager of data files for a job

    For each job, there is a local directory where the job is
    constructed.

    When this job is submitted, the whole directory in the local
    machine is copied over to the computation server.
    The path where the job in the computation server will be
    run is stored the the database "servers":
      %vnf.dom.Server.workdir%/%job_id
    
    Computations will be done in the computation server, and
    results of computations will be saved there.

    '''

    def __init__(self, job, db, csaccessor = None, dds=None):
        self.job = job
        self.db = db
        self.dds = dds
        self.csaccessor = csaccessor
        return


    def initlocaldir(self):
        path = self.localpath()
        if os.path.exists( path ): return
        try:
            os.makedirs( path )
        except:
            raise RuntimeError, "unable to create directory %r" % os.path.abspath(path)
        return path


    def initremotedir(self):
        csaccessor = self.csaccessor
        if csaccessor is None: raise RuntimeError('need csaccessor to do things.')
        #remote job directory is initd by copying local job dir
        
        #localpath
        path = self.localpath()
        
        #check local path
        if not os.path.exists(path):
            raise RuntimeError, (
                "local directory for job %s has not been established" % (
                self.job.id) )

        db = self.db
        server = self.job.server.dereference(db)
        # copy local job directory to server
        # 1. create the directory
        cmd = 'mkdir -p %s' % self.remotepath()
        csaccessor.execute(cmd, server, '/')
        return
        # 2. copy files
        files = self.listlocaljobdir()
        files = filter(lambda f: not f.startswith(self.dds.dds.prefix_remember), files)
        debug.log('copying files %s ...' % (files,))
        self.dds.make_available(self.job, files, server=server)
        #csaccessor.pushdir(
        #    path, server, self.remotepath() )
        return


    def listlocaljobdir(self):
        return os.listdir(self.localpath())
    

    def listremotejobdir(self):
        '''list files in the remote job directory'''

        csaccessor = self.csaccessor
        if csaccessor is None: raise RuntimeError('need csaccessor to do things.')

        db = self.db
        server = self.job.server.dereference(db)
        remotedir = self.remotepath()
        failed, output, error = csaccessor.execute(
            'ls', server, remotedir )
        if failed:
            raise RuntimeError, 'unable to list directory %s in server %s' % (
                remotedir, server.server)
        #the list of files in the job directory
        entries = output.split()
        return entries


    def remotepath(self):
        db = self.db
        job = self.job
        server = job.server.dereference(db)
        return self.dds.abspath(self.job, server=server)


    def localpath(self):
        return self.dds.abspath(self.job)


import os


# version
__id__ = "$Id$"

# End of file 
