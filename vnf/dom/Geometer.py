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


class Geometer(object):


    def __init__(self):
        return


    def __get__(self, instance, cls = None):
        if not isinstance( instance, Table ):
            raise RuntimeError, "%s is not a db record"

        table = instance.__class__

        try:
            table.id
        except AttributeError:
            msg = "Table %s does not have a 'id' column." % (
                table, )
            raise RuntimeError, msg

        id = instance.id
        return registry( id, table )


    def __set__(self, *args, **kwds):
        msg = """geometer is not setable by syntax
    container.geometer = new_geometer
To update geometer, use the methods of geometer. use help to find out:
    help( container.geometer )
"""
        raise RuntimeError, msg


from PositionOrientationRegistry import registry
from Table import Table


# version
__id__ = "$Id$"

# End of file 
