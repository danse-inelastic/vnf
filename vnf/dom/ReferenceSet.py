#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


'''
ReferenceSet

Model a 1-M relation.

Useful to describe parent-children relationship.
'''


class ReferenceSet(object):


    # This is just a descriptor.


    def __init__(self, name):
        self.name = name
        return


    def __get__(self, instance, cls = None):
        if not isinstance( instance, Table ):
            raise RuntimeError, "%s is not a db record"

        table = instance.__class__

        try:
            table.id
        except AttributeError:
            msg = "Table %s does not have a 'id' column. Cannot get reference set" % (
                table, )
            raise RuntimeError, msg

        id = instance.id
        return referenceset( self.name, id, table )


    def __set__(self, *args, **kwds):
        msg = """Reference set is not setable by syntax
    container.references = new_references
To update references, use the methods of references. use help to find out:
    help( container.references )
"""
        raise RuntimeError, msg



from Table import Table
from _referenceset import referenceset


# version
__id__ = "$Id$"

# End of file 
