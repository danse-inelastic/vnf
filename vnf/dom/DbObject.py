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
    
    id = pyre.db.varchar(name="id", length=64)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    short_description = pyre.db.varchar(name='short_description', length = 128, default='')
    short_description.meta['tip'] = 'short_description'

    pass # end of DbObject


# version
__id__ = "$Id$"

# End of file 
