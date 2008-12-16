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
        return

    def render(self, computation, db=None, dds=None):
        from kernelGenerator.trajectory.nMoldynDerived.misc import saveText
        saveText
        
        path = self._path(self.shscriptname)
        open(path, 'w').write('\n'.join(cmds))
        
        type = computation.type
        return handler(type)(self.path).render(computation, db=db, dds=dds)





# version
__id__ = "$Id$"

# End of file 
