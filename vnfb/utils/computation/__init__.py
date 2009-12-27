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


def retrieve_results(computation, director, debug=False):
    'retrieve results of computation'
    
    # get handler
    name = computation.getResultRetrieverName()
    retriever = director.retrieveComponent(
        name, factory='retriever', vault=['result_retrievers'])
    if retriever is None:
        curator_dump = director._dumpCurator()
        raise RuntimeError, "could not load result retriever %r. curator dump: %s" % (
            name, curator_dump)
    retriever.director = director

    # run retriever
    return retriever.run(computation, debug=debug)


# version
__id__ = "$Id$"

# End of file 
