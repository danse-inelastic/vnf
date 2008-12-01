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



'''
a job is something that can be delivered to computation server and be launched.

It needs to contain:

  - a bash script to be launched on the computation server
  - all necessary files that are needed for the bash script to run, such as
    * configuration files
    * data files

'''


class JobBuilder(object):

    shscriptname = 'run.sh'
    dependencies_path = '__dependencies__'

    def __init__(self, path):
        self.path = path
        self._init_rootdir()
        return
    

    def render(self, computation, db=None):
        raise NotImplementedError


    def registerDependency(self, dependency):
        '''register a dependency to my dependency list

        A dependency is a db record. For example, a job requires a density of
        states curve, and that curve is stored as db record DOS(id=ABCDE).
        The data files for the db record DOS(id=ABCDE) need to be made 
        available at the computation server.
        '''
        type = dependency.name
        id = dependency.id
        path = self._path(self.dependencies_path)
        entry = '%s,%s\n' % (type, id)
        lines = open(path).readlines()
        if entry not in lines:
            f = open(path, 'a')
            f.write(entry)
            del f
        return


    def getDependencies(self):
        path = self._path(self.dependencies_path)
        if not os.path.exists(path): return []
        f = open(path)
        deps = f.read().split('\n')
        return [dep.split(',') for dep in deps if dep]
    

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
