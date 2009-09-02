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


class Node:

    def __init__(self, address, rootpath):
        self.address = address
        self.rootpath = rootpath
        return

    def __str__(self):
        return '%s:%s' % (self.address, self.rootpath)
    
    pass # end of DataStorage


# version
__id__ = "$Id$"

# End of file 
