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


    from vnf.dom.ins.BvKComputation import BvKComputation as Computation

    def retrieve(self):
        computation = self.computation
        type = computation.type
        handler = getattr(self, '_on%s'%type)
        return handler()


    def _ondos(self):
        director = self.director
        computation = self.computation
        job = director.clerk.dereference(computation.job)

        from vnf.dom.ins.PhononDOS import PhononDOS
        expected_results = [
            ('DOS', (PhononDOS, 'data.idf')),
            ]
        filenames = [filename for filename, dummy in expected_results]
        self._check_job_results_sanity(job=job, expected_results=filenames)

        # save results
        for filename, (table, newfilename) in expected_results:
            # for each result, check if it already was recorded as a result
            if not self._is_result_saved(job, filename):
                # if not, save it
                self._save_result(job, filename, table, newfilename)

        computation.results_state = 'retrieved'
        self.director.clerk.updateRecord(computation)
        return


    def _ondirectional(self):
        return


    def _ongrid(self):
        return
    


# version
__id__ = "$Id$"

# End of file 
