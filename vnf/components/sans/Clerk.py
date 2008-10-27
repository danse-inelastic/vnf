# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class Clerk: pass


class DeepCopier:

    def onSANSSphereModelKernel(self, kernel):
        return self._onRecordWithID( kernel )
    

# version
__id__ = "$Id$"

# End of file 
