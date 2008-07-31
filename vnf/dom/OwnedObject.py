# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from DbObject import DbObject
class OwnedObject(DbObject):

    import pyre.db

    creator = pyre.db.varchar(name='creator', length = 32)
    creator.meta['tip'] = 'creator name'

    date = pyre.db.date( name='date' )
    date.meta['tip'] = 'date of creation'

    pass # end of Shape


# version
__id__ = "$Id$"

# End of file 
