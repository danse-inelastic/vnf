#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def visual(director=None):
    from .StructureUploaderFactory import Factory
    oncomplete=('atomicstructure/uploadmatter-public', 'onUpload')
    f = Factory(director, oncomplete=oncomplete)
    return f.build()


# version
__id__ = "$Id$"

# End of file 

