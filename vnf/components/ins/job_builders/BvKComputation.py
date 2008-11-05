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

    from vnf.dom.ins.BvKComputation import BvKComputation as Computation

    def __init__(self, path):
        self.path = path
        return

    def render(self, computation, db=None, dds=None):
        type = computation.type
        return handler(type)(self.path).render(computation, db=db, dds=dds)


def handler(type):
    from BvKDOSJobBuilder import Builder as DOS
    d = {'dos': DOS,
         }
    return d[type.lower()]


# version
__id__ = "$Id$"

# End of file 
