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


from Table import Table
class DbObject(Table):

    import pyre.db
    
    id = pyre.db.varchar(name="id", length=100)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    short_description = pyre.db.varchar(name='short_description', length = 128)
    short_description.meta['tip'] = 'short_description'

    pass # end of Shape


# version
__id__ = "$Id$"

# End of file 
