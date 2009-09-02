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

class Builder(base):


    def __init__(self, path):
        super(Builder, self).__init__(path)
        from BvKModelRenderer import Renderer
        self.modelbuilder = Renderer(path)
        return
    

    def render(self, computation, db=None, dds=None):
        model = computation.model.dereference(db)
        files = self._render_model(model, dds=dds)
        files.append( self._make_script(computation) )
        return files


    def _make_script(self, bvkcomputation):
        N1 = bvkcomputation.N1
        dE = bvkcomputation.dE
        cmds = [
            'source ~/.bvk',
            'bvkdisp.py -d %s -N %s %s' % (dE, N1, self.modelbuilder.systempy),
            ]
        path = self._path(self.shscriptname)
        open(path, 'w').write('\n'.join(cmds))
        return self.shscriptname
    
    
    def _render_model(self, model, dds=None):
        return self.modelbuilder.render(model, dds=dds)

    pass # end of JobBuilder


# version
__id__ = "$Id$"

# End of file 
