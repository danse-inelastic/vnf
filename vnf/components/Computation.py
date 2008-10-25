#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2008  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def retrieve_results(computation, director, debug=False):
    from vnf.utils import launch_detached, bindir
    import os
    exe = os.path.join(bindir, 'retrieveresults.py')
    launch_detached(
        '%s -type=%s -id=%s' % (exe, computation.__class__.__name__, computation.id),
        debug=debug)
    return


def _():
    type = computation.__class__.__name__
    exec 'from computation_result_retrievers.%s import Retriever' % type
    ret = Retriever(computation, director).retrieve()
    computation.results_retrieved = True
    director.clerk.updateRecord(computation)
    return ret


# version
__id__ = "$Id$"

# End of file 
