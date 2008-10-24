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


class JobBuilder:

    def __call__(self, computation, db=None, dds=None, path=None):
        t = computation.__class__.__name__
        exec 'from vnf.components.job_builders.%s import Builder' % t
        return Builder(path).render(computation, db=db, dds=dds)
        


# version
__id__ = "$Id$"

# End of file 
