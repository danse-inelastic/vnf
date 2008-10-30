#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from opal.weaver.DocumentMill import DocumentMill as base


class DocumentMill(base):

    def __init__(self, tagger, configurations):
        base.__init__(self, tagger)
        self.configurations = configurations
        return

    pass # end of DocumentMill


def extended(extensions):
    return subclassOf( [DocumentMill] + extensions )


def subclassOf(classes):
    for i, C in enumerate(classes): exec 'C%d=C' % i in locals()
    code = 'class N(%s): pass' % ', '.join([ 'C%d' % i for i in range(len(classes)) ])
    exec code in locals()
    return N


# version
__id__ = "$Id$"

# End of file 
