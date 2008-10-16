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
        if not os.path.exists(self.path):
            try:
                os.makedirs(self.path)
            except Exception, err:
                raise RuntimeError, "unable to create directory %r. %s: %s" % (
                    self.path, err.__class__.__name__, err)
        return
    
    pass # end of JobBuilder

import os

# version
__id__ = "$Id$"

# End of file 
