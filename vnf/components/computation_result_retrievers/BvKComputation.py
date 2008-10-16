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


from Retriever import Retriever as base

class Retriever(base):

    def retrieve(self):
        computation = self.computation
        if computation.results_retrieved: return
        type = computation.type
        handler = getattr(self, '_on%s'%type)
        return handler()


    def _ondos(self):
        director = self.director
        computation = self.computation
        job = computation.job.dereference(director.db)

        expected_results = [
            'DOS',
            ]
        self._check_job_results_sanity(job=job, expected_results=expected_results)

        result_records_ref = computation.results
        result_records = result_records_ref.dereference(director.db)

        # save results
        from vnf.dom.PhononDOS import PhononDOS
        expecetd_result_types = [
            PhononDOS,
            ]
        for t in expecetd_result_types:
            # for each result, check if it already was recorded as a result
            if not self._is_result_recorded(t, result_records):
                # if not, record it
                self._record_result(job, 'DOS', t, 'data.idf')
        return


    def _ondirectional(self):
        return


    def _ongrid(self):
        return
    


# version
__id__ = "$Id$"

# End of file 
