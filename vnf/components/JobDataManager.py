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

class JobDataManager:

    relative_results_path = '__results__'

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

    In the local directory for this job, there should be
    a directory %relative_results_path%. Whenever a request for computation
    result is received, this data manager should try to fetch
    that result and store it in this local result directory.
    '''

    def __init__(self, job, db, csaccessor = None):
        self.job = job
        self.db = db
        self.csaccessor = csaccessor
        return


    def initlocaldir(self):
        path = self.localpath()
        if os.path.exists( path ): return
        try:
            os.makedirs( path )
        except:
            raise RuntimeError, "unable to create directory %r" % os.path.abspath(path)
        #make results directory too
        path2 = self.localresultdir()
        os.makedirs( path2 )
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
        csaccessor.pushdir(
            path, server, server.workdir )
        return
    

    def makelocalcopy(self, filename):
        '''make a local copy of a data file from the remote machine'''

        csaccessor = self.csaccessor
        if csaccessor is None: raise RuntimeError('need csaccessor to do things.')
        
        #retieve file from computation server
        #should we also retrieve all files from computation server?
        #probably not. because, for example, the wave-function
        #file could be huge.
        db = director.db
        server = self.job.server.dereference(db)
        remotedir = self.remotepath()
        localdir = self.localresultdir()
        localcopy = csaccessor.getfile(
            server, os.path.join(remotedir, filename), localdir)
        return localcopy


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
        job = self.job
        db = self.db
        server = job.server.dereference(db)
        return os.path.join(server.workdir, job.id )


    localbasepath = '../content/jobs'
    def localpath( self ):
        jobid = self.job.id
        jobdir = os.path.join( self.localbasepath, jobid )
        return jobdir


    def localresultdir(self):
        return os.path.join(self.localpath(), self.relative_results_path)


import os


# version
__id__ = "$Id$"

# End of file 
