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

import luban.content as lc


def getBaseVectorsDoc(matter, primitive_unitcell=False, title=None, id=None):
    if primitive_unitcell:
        base = matter.primitive_unitcell.base
    else:
        base = matter.lattice.base
    doc = lc.document(id=id, title=title)
    for v in base:
        doc.paragraph(text=[str(v)])
        continue
    return doc



# version
__id__ = "$Id$"

# End of file 
