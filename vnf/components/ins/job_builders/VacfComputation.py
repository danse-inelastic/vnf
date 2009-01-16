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

    from vnf.dom.ins.VelocityAutocorrelation import VelocityAutocorrelation as Computation

    def __init__(self, path):
        self.path = path
        self.deps = []
        return
    
    def getDependencies(self):
        return self.deps

    def render(self, computation, db=None, dds=None):
        trajectory = computation.trajectory.dereference(self.db)
        self.deps.append(trajectory)
        # 
        runsh = self._make_script(computation)
        return [runsh]


    def _make_script(self, computation):
        import os
        # self.dds.relativepath(job, trajectory, filename)
        trajectory = os.path.join('..', '..', self.dds.path(computation.trajectory), 'trajectory.nc')
        d = {
             'units': computation.units,
             'weights': computation.weights,
             'trajectory': trajectory,
             }
        #note to self: combine the programs that write out file and execute it in one python script
        cmds = [
            'source ~/.moldyn',
            'vacf.py --units=%(units)s --weights=%(weights)s --trajectory=%(trajectory)s' % d
            ]
        path = self._path(self.shscriptname)
        open(path, 'w').write('\n'.join(cmds))
        return self.shscriptname
    
    
        #retrieve vacf settings
        #use saveText to
        #from kernelGenerator.trajectory.nMoldynDerived.misc import saveText
        #saveText
        
        #path = self._path(self.shscriptname)
        #open(path, 'w').write('\n'.join(cmds))
        
        #type = computation.type
        #return handler(type)(self.path).render(computation, db=db, dds=dds)





# version
__id__ = "$Id$"

# End of file 
