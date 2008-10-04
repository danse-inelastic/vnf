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


from Job import Job


from OwnedObject import OwnedObject as base
class Computation(base):

    # base class for all computations (including simulations)

    import vnf.dom
    results = vnf.dom.referenceSet(name='results')

    import pyre.db
    job = pyre.db.reference(name='job', table = Job)
    

# version
__id__ = "$Id$"

# End of file 
