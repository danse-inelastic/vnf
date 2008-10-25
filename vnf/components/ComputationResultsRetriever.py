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


class ComputationResultsRetriever:

    def __call__(self, computation, director=None):
        states = [
            'retrieved',
            'retrieval failed',
            'retrieving',
            ]
        if computation.results_state in states: return

        computation.results_state = 'retrieving'
        director.clerk.updateRecord(computation)
        
        type = computation.__class__.__name__
        exec 'from vnf.components.computation_result_retrievers.%s import Retriever' % type
        Retriever(computation, director).retrieve()
        
        return


# version
__id__ = "$Id$"

# End of file 
