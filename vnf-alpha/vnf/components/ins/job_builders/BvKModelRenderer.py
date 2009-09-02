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


from JobBuilder import JobBuilder as base

class Renderer(base):

    systempy = 'system.py'

    def render(self, model, dds=None):
        path = self._make_systempy(model, dds=dds)
        return [self.systempy]
    
    
    def _make_systempy(self, model, dds=None):
        content = [
            'from bvk.input_generators.system import System',
            ]
        content += self._read_system(model, dds=dds)
        
        path = self._path( self.systempy )

        open(path, 'w').write('\n'.join(content))
        return path
    
    
    def _read_system(self, model, dds=None):
        systempy = dds.abspath(model, self.systempy)
        return open(systempy).readlines()
    
    pass # end of JobBuilder


import os

# version
__id__ = "$Id$"

# End of file 
