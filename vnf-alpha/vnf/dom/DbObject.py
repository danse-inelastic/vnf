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

    import dsaw.db
    
    id = dsaw.db.varchar(name="id", length=64)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    short_description = dsaw.db.varchar(name='short_description', length = 128, default='')
    short_description.meta['tip'] = 'short_description'

    pass # end of DbObject


if __name__=='__main__':
    dbOb = DbObject()
    dbOb.id = '3328'
    print dbOb
    print dbOb.id

# version
__id__ = "$Id$"

# End of file 
