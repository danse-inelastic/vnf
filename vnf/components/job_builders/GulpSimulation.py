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

    from vnf.dom.GulpSimulation import GulpSimulation as Computation

    def __init__(self, path):
        base.__init__(self, path)
        return

    def render(self, computation, db=None, dds=None):
        files = [self.gulp_inputfile]
        files.append( self._make_script(computation) )
        return files

    gulp_inputfile = "gulp.gin"
    def _make_script(self, bvkcomputation):
        cmds = [
            'source ~/.gulp-env',
            'gulp < %s' % self.gulp_inputfile
            ]
        path = self._path(self.shscriptname)
        open(path, 'w').write('\n'.join(cmds))
        return self.shscriptname


# version
__id__ = "$Id$"

# End of file 
