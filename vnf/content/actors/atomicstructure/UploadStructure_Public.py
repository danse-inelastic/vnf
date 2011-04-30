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


import luban.content
import os

from luban.components.Actor import Actor as base
from UploadStructure_Mixin import Mixin

class Actor(base, Mixin):


    class Inventory(base.Inventory, Mixin.Inventory):

        pass


    def onUpload(self, director):
        '''
        structureid: atomic structure id

        return: action to replace the current view with 
            thew view of the new atomic structure
        '''
        try:
            newrecordid = super(Actor, self).onUpload(director)
        except RuntimeError, e:
            return luban.content.alert(str(e))
        
        return luban.content.load(
            actor='atomicstructure-public', 
            )


# version
__id__ = "$Id$"

# End of file 

