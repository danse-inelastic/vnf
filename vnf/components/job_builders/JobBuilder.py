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


class JobBuilder(object):

    shscriptname = 'run.sh'


    def __init__(self, path):
        self.path = path
        self._init_rootdir()
        return
    

    def render(self, computation, db=None):
        raise NotImplementedError


    def _path(self, filename):
        return os.path.join(self.path, filename)
    
    
    def _init_rootdir(self):
        if not os.path.exists(self.path): os.makedirs(self.path)
        return
    
    pass # end of JobBuilder

import os

# version
__id__ = "$Id$"

# End of file 
