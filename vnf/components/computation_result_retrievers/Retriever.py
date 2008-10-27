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


def all_results_exist(results, job, director):
    server = director.clerk.dereference(job.server)
    for r in results:
        if not director.dds.is_available(job, r, server): return False
        continue
    return True


class Retriever:

    def __init__(self, computation, director):
        self.computation = computation
        self.director = director
        return


    def _check_job_results_sanity(self, expected_results=None, job=None):
        director = self.director
        if isdone(job) and not all_results_exist(expected_results, job, director):
            raise RuntimeError, "job %s was done but not all expected results were generated"
        

    def _record_result(self, job,filenameinjobdir, recordtype,newfilename):
        #create a new record to save the result
        director = self.director
        record = director.clerk.newOwnedObject(recordtype)

        #make symbolic link from the result db record's data directory
        #to the job directory
        server = director.clerk.dereference(job.server)
        director.dds.symlink(job,filenameinjobdir, record,newfilename, server)

        # the result record should know where it comes from
        record.origin = self.computation
        director.clerk.updateRecord(record)

        # add the result to the result list
        self.computation.results.add(record, director.clerk.db, name=record.name)
        return


    def _is_result_recorded(self, resulttype, records):
        for r in records:
            if r.__class__ == resulttype: return True
            continue
        return False


    pass # end of Retriever


from vnf.components.Job import isdone


# version
__id__ = "$Id$"

# End of file 
