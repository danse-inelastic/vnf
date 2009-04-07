#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                     (C) 2007-2009  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



def Inherited(classes):
    for i, C in enumerate(classes): exec 'C%d=C' % i in locals()
    code = 'class N(%s): pass' % ', '.join([ 'C%d' % i for i in range(len(classes)) ])
    exec code in locals()
    return N


# version
__id__ = "$Id$"

# End of file 
