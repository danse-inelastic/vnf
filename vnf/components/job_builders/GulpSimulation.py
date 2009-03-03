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
        Computation = self.Computation

        # find out the file name of the gulp library file
        libptr = dds.abspath(computation, filename=Computation.LIBPOINTER_FILE)
        libname = open(libptr).read().strip()

        # two files need to be copied to job directory
        # 1. gulp.gin
        # 2. the library file
        files = [Computation.CONFIGURATION_FILE, libname]

        # copy files to job directory
        job = computation.job.dereference(db)
        for f in files:
            dds.copy(computation, f, job, f)

        # add run.sh
        files.append( self._make_script(computation) )
        return files

    def _make_script(self, computation):
        Computation = self.Computation
        
        cmds = [
            'source ~/.gulp-env',
            'gulp < %s > gulp.out' % Computation.CONFIGURATION_FILE
            ]
        path = self._path(self.shscriptname)
        open(path, 'w').write('\n'.join(cmds))
        return self.shscriptname


# version
__id__ = "$Id$"

# End of file 
