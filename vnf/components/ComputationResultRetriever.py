# -*- Python -*-
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


class ResultsMissing(Exception): pass
class RetrievalFailed(Exception): pass


from pyre.components.Component import Component

class ComputationResultRetriever(Component):

    director = None # should be signed when initd

    def run(self, computation):
        director = self.director
        self._initFacilitiesFromDirector(director)

        self.declareProgress(0.05, 'check status of retrieval')
        # first check if it is necessary to run this component
        states = [
            'retrieved',
            #'retrieval failed',
            'retrieving',
            ]
        state = computation.getResultRetrievalStatus(self.db)
        if state in states:
            self._debug.log('no need to run retriever. computation %s: %s' % (
                computation.id, state))
            return

        # set the results_state so that this retriever won't be run twice
        self.declareProgress(0.06, 'set status of retrieval to prevent reentry')
        computation.setResultRetrievalStatusAndErrorMessage('retrieving', '', db = self.db)

        # retrieve results
        try:
            self._retrieveResultsFor(computation)
        except Exception, e:
            # the error message
            import traceback
            if hasattr(computation, 'creator'):
                creator = computation.creator
            else:
                creator = 'unknown'
            subject = 'computation result retrieval failed: user=%s, computation=%s#%s' % (
                creator, computation.__class__.__name__, computation.id)
            body = [
                "%s: %s\n%s" % (e.__class__.__name__, e, traceback.format_exc()),
                ]

            # send an alert email
            # from vnf.utils.communications import announce
            # announce(director, 'alert-to-vnf-developers',
            #          message=body, subject=subject)
            
            # also send to journal
            error = '\n'.join([subject] + body)
            self._debug.log(error)

            # save to db
            computation.setResultRetrievalStatusAndErrorMessage(
                'retrieval failed', error, db=self.db)
            
            raise RetrievalFailed, error

        else:
            # if we reach here it means everything is good
            computation.setResultRetrievalStatusAndErrorMessage('retrieved', message='', db=self.db)

            self.declareProgress(1.0, 'retrieval succeeded')
        return


    def _declareProgress(self, percentage, message):
        # default implementation for declareProgress when no other machinery is
        # available
        self._debug.log('%s: %s' % (percentage, message))
        return


    def _retrieveResultsFor(self, computation):
        raise NotImplementedError


    def _check_results_sanity(self, expected_results=None, job=None):
        '''check if the status of computation results is sane

        expected_results: expected data files generated from computation
        job: the computation job db record
        '''
        director = self.director
        if job.isdone():
            missing = self._missing_results(expected_results, job)
            if missing:
                msg = "job %s was done but not all expected results were generated: %s" % (
                    job.id, missing)
                raise ResultsMissing, msg
        return
    

    def _missing_results(self, results, job):
        '''check if all computation results (data files) already exist.
        return a list of results that are still missing.

        results: data file names that should be generated by the computation
        job: the job db record
        '''
        server = self.db.dereference(job.server)
        is_available = self.dds.is_available
        return filter(lambda f: not is_available(job, f, server), results)
    

    def _make_result_holder(self, computation, table, name=None):
        '''make a result holder (a db record)
        
        For example, a bvk computation will create a dos data file, and it
        should be saved as a DOS data object. The result holder is then
        a record of the PhononDOS db table. This function create a new db record
        of given db table.

        computation: the computation of interest
        table: the db table of result holder
        '''
        record = self.clerk.insertNewOwnedRecord(table, owner = computation.creator)
        
        # the result record should know where it comes from
        record.origin = computation
        self.db.updateRecord(record)
        
        return record
        

    def _save_result(self, computation, job, filenameinjobdir, result_holder, newfilename=None, name=None):
        '''save a computation result data file as a data file for a db record.

        computation, job: the computation and the job db records
        filenameinjobdir: the data file name generated from the computation that was saved
            in the job data directory
        result_holder: the db record in which the result will be saved
        newfilename: the new data file name in the data directory for the result holder.
            This indicates the new path the computation result will be saved
        name: name of this result in the result set (optional)
        '''
        # copy result file from job to the result holder
        if newfilename:
            resultFileName = newfilename
        else:
            resultFileName = filenameinjobdir
        server = self.db.dereference(job.server)
        self.dds.copy(job, filenameinjobdir, result_holder, resultFileName, server)
        # make copy of result holder in the master node
        self.dds.make_available(result_holder, [resultFileName])

        # add the result to the result list
        if not name:
            name = result_holder.getTableName()

        computation.results.add(result_holder, self.db, name=name)
        self._mark_result_as_saved(computation, filenameinjobdir)
        return
    

    def _symlink_results(self, computation, job, files, result_holder, name=None):
        '''symlink computation result data files to a db record.

        computation, job: the computation and the job db records
        files: a list of file names or a dictionary of {filenameinjobdir: filenameinresultholder}
        result_holder: the db record in which the result will be saved
        name: name of this result in the result set (optional)
        '''
        # copy result file from job to the result holder
        server = self.db.dereference(job.server)
        filesisdict = isinstance(files, dict)
        destinationFiles = []
        for f in files:
            finjobdir = f
            if filesisdict:
                finresultholder = files[f]
            else:
                finresultholder = f
            destinationFiles.append(finresultholder)
            #self.dds.copy(job, finjobdir, result_holder, finresultholder, server)
            self.dds.symlink(job, finjobdir, result_holder, finresultholder, server)
            
        # remember where it is (i.e. on octopod)
        self.dds.remember(result_holder, server)
        
        # add the result to the result list
        if not name:
            name = result_holder.getTableName()

        computation.results.add(result_holder, self.db, name=name)
        for f in files:
            self._mark_result_as_saved(computation, f)
        return

    def _save_and_move_results(self, computation, job, files, result_holder, name=None):
        '''move computation result data files to a db record.

        computation, job: the computation and the job db records
        files: a list of file names or a dictionary of {filenameinjobdir: filenameinresultholder}
        result_holder: the db record in which the result will be saved
        name: name of this result in the result set (optional)
        '''
        # copy result file from job to the result holder
        server = self.db.dereference(job.server)
        filesisdict = isinstance(files, dict)
        destinationFiles = []
        for f in files:
            finjobdir = f
            if filesisdict:
                finresultholder = files[f]
            else:
                finresultholder = f
            destinationFiles.append(finresultholder)
            #self.dds.copy(job, finjobdir, result_holder, finresultholder, server)
            self.dds.move(job, finjobdir, result_holder, finresultholder, server)
            
        # remember where it is (i.e. on octopod)
        self.dds.remember(result_holder, server)
        
        # make copy of result holder in the master node
        self.dds.make_available(result_holder, files=destinationFiles)
        
        # add the result to the result list
        if not name:
            name = result_holder.getTableName()

        computation.results.add(result_holder, self.db, name=name)
        for f in files:
            self._mark_result_as_saved(computation, f)
        return
    

    def _save_results(self, computation, job, files, result_holder, name=None, result_subdir=None):
        '''save computation result data files to a db record.

        computation, job: the computation and the job db records
        files: a list of file names or a dictionary of {filenameinjobdir: filenameinresultholder}
        result_holder: the db record in which the result will be saved
        name: name of this result in the result set (optional)
        result_subdir: the subdirectory in the result_holder directory where the files will be saved. (optional)
        '''
        import os
        server = self.db.dereference(job.server)
        
        # create directory in result_holder at the server
        self.dds.makedirs(result_holder, server, subdir=result_subdir)
        
        # copy result file from job to the result holder
        filesisdict = isinstance(files, dict)
        destinationFiles = []
        for f in files:
            finjobdir = f
            if filesisdict:
                finresultholder = files[f]
            else:
                finresultholder = f
            # if subdir is specified, need to adjust the path
            if result_subdir:
                finresultholder = os.path.join(result_subdir, finresultholder)
            destinationFiles.append(finresultholder)
            self.dds.copy(job, finjobdir, result_holder, finresultholder, server)
            
        # make copy of result holder in the master node
        self.dds.make_available(result_holder, files=destinationFiles)
        
        # add the result to the result list
        if not name:
            name = result_holder.getTableName()

        computation.results.add(result_holder, self.db, name=name)
        for f in files:
            pass
            self._mark_result_as_saved(computation, f)
        return


    def _mark_result_as_saved(self, computation, filename):
        '''make a computation result filename as saved'''
        return computation.markResultFileAsSaved(filename, self.db)
    

    def _is_result_saved(self, computation, filename):
        '''check if a computation result filename was saved'''
        return computation.isResultFileSaved(filename, self.db)


    def __init__(self, name):
        super(ComputationResultRetriever, self).__init__(
            name, facility='computation-result-retriever')
        return


    def _initFacilitiesFromDirector(self, director):
        ''' result retriever needs a bunch of facilities to work properly.
        they are obtained from the director
        '''
        self.clerk = director.clerk
        self.orm = self.clerk.orm
        self.db = self.clerk.db
        self.dds = director.dds
        # this may be run in a itaskapp
        if hasattr(director, 'declareProgress'):
            self.declareProgress = director.declareProgress
        else:
            self.declareProgress = self._declareProgress
        return


# version
__id__ = "$Id$"

# End of file 