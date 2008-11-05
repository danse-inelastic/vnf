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
debug = journal.debug('retrieveresults')


class ComputationResultsRetriever:

    def __call__(self, computation, director=None):
        states = [
            'retrieved',
            #'retrieval failed',
            'retrieving',
            ]
        if computation.results_state in states: 
            debug.log('computation %s: %s' % (computation.id, computation.results_state))
            return

        computation.results_state = 'retrieving'
        director.clerk.updateRecord(computation)

        from vnf import extensions as depositories
        Retriever = findRetriever(computation.__class__, depositories)
        Retriever(computation, director).retrieve()
        
        return


def findRetriever(Computation, depositories):
    
    candidates = []
    for depository in depositories:
        package = ['vnf', 'components']
        if depository: package.append(depository)
        package += ['computation_result_retrievers']
        package = '.'.join(package)

        module = Computation.__name__

        code = 'from %s.%s import Retriever' % (package, module)
        try:
            print code
            exec code in locals()
        except:
            import journal
            import traceback
            journal.debug('main').log(traceback.format_exc())
            continue
        candidates.append(Retriever)
        continue

    l = filter(lambda Retriever: Retriever.Computation==Computation, candidates)
    if len(l) != 1:
        if not len(l):
            raise RuntimeError, 'No result retriever found for computation %s' % Computation
        if len(l) > 1:
            raise RuntimeError, 'More than one result retrievers for computation %s exist' % Computation
    return l[0]


# version
__id__ = "$Id$"

# End of file 
