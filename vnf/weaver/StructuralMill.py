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


def subclassOf(classes):
    for i, C in enumerate(classes): exec 'C%d=C' % i in locals()
    code = 'class N(%s): pass' % ', '.join([ 'C%d' % i for i in range(len(classes)) ])
    exec code in locals()
    return N


from opal.weaver.StructuralMill import StructuralMill  as base
from DocumentMill import DocumentMill
from DocumentMillExtensions import extensions


class StructuralMill(subclassOf([DocumentMill]+extensions), base):
    
    def __init__(self, tagger, configurations):
        DocumentMill.__init__(self, tagger, configurations)
        return


# version
__id__ = "$Id$"

# End of file 
