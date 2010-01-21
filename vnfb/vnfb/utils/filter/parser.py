# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import sys

vinfo = sys.version_info

if vinfo[0] == 2:
    if vinfo[1] == 5:
        from parser_25 import *
    elif vinfo[1] == 6:
        from parser_26 import *
    else:
        raise NotImplementedError
else:
    raise NotImplementedError


# version
__id__ = "$Id$"

# End of file 
