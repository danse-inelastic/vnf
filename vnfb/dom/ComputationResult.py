# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# this is an interface class. any data object table type that could be
# a result of a computation should use this class as one of its base classes.
# The implementation here depends on the implementation in the "Computation" table.
class ComputationResultInterface:

    def getOrigin(self, db):
        'get the original computation that gives this result (self)'
        # implementation: since Computation table uses "results" to
        # hold references to computation results, we can seach
        # the referenceset table to find the computation orgin
        # for a computation result
        from dsaw.db._referenceset import _ReferenceSetTable

        # my global "address"
        gp = self.globalpointer and self.globalpointer.id
        if gp is None:
            return

        #
        where = "element=%s and containerlabel='computation_results'" % gp
        r = db.query(_ReferenceSetTable).filter(where).one()

        return r.container.dereference(db)



# this defines a common base for computation result classes.
# usually it is a good enough base class. it is also ok to subclass
# ComputationResultInterface and other table base
from AbstractOwnedObjectBase import AbstractOwnedObjectBase
class ComputationResult(ComputationResultInterface, AbstractOwnedObjectBase): 
    pass


# version
__id__ = "$Id$"

# End of file 
