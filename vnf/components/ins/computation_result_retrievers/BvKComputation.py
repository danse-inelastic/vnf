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
                result_holder = self._make_result_holder(job, table)
                self._save_result(job, filename, result_holder, newfilename)

        computation.results_state = 'retrieved'
        self.director.clerk.updateRecord(computation)
        return


    def _ondirectional(self):
        raise NotImplementedError


    def _ondisp(self):
        director = self.director
        computation = self.computation
        job = director.clerk.dereference(computation.job)

        expected_files = [
            'DOS',
            'Omega2',
            'Polarizations',
            'WeightedQ',
            ]
        self._check_job_results_sanity(job=job, expected_results=expected_files)

        #create the result holder
        from vnf.dom.ins.PhononDispersion import PhononDispersion
        dispersion = self._make_result_holder(job, PhononDispersion)
        
        # save results
        for filename in expected_files:
            # for each result, check if it already was recorded as a result
            if not self._is_result_saved(job, filename):
                # if not, save it
                self._save_result(job, filename, dispersion, filename)

        # make file 'Qgridinfo'
        self._makeQgridinfo(dispersion)

        computation.results_state = 'retrieved'
        self.director.clerk.updateRecord(computation)
        return


    def _makeQgridinfo(self, dispersion):
        #
        director = self.director
        computation = self.computation

        # reciprocal lattice
        matter = director.clerk.dereference(computation.matter)
        lattice = _lattice(matter.cartesian_lattice)
        b1, b2, b3 = _reciprocal(lattice)
        contents = []
        contents.append('b1=%s' % (tuple(b1),))
        contents.append('b2=%s' % (tuple(b2),))
        contents.append('b3=%s' % (tuple(b3),))

        # grid sizes
        N1 = computation.N1
        contents.append('n1=n2=n3=%d' % N1)

        filename = 'Qgridinfo'
        dir = director.dds.abspath(dispersion)
        import os
        if not os.path.exists(dir): os.makedirs(dir)
        f = director.dds.abspath(dispersion, filename)
        open(f, 'w').write('\n'.join(contents))
        # remember
        director.dds.remember(dispersion, filename=filename)
        return
    

import numpy as N
def _lattice(array):
    a = N.array(array)
    a.shape = 3, 3
    return a
    
def _reciprocal(lattice):
    v = _volume(lattice)
    a1, a2, a3 = lattice
    b1 = N.cross(a2,a3)/v
    b2 = N.cross(a3,a1)/v
    b3 = N.cross(a1,a2)/v
    return b1, b2, b3

def _volume(vectors):
    v0, v1, v2 = vectors
    return N.dot(v0, N.cross(v1, v2))

# version
__id__ = "$Id$"

# End of file 
