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

from Table import Table

class GulpPotential(Table):

    name = 'gulppotential'

    path = '../content/data/gulppotentials'

    import dsaw.db
    filename = dsaw.db.varchar(name='filename', length=2048, default='potential.lib')
    
    elements = dsaw.db.varcharArray(name = 'elements', length = 10, default = [] )
    elements.meta['tip'] = 'elements within the potential'
    
    description = dsaw.db.varchar(name = 'description', length=10240)
    
    creator = dsaw.db.varchar(name='creator', length=128)

    date = dsaw.db.date( name='date' )
    date.meta['tip'] = 'date of creation'
    
    id = dsaw.db.varchar(name="id", length=100)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

#    this should be the name of the primary key...for now we *have* to name it 'id'
#    potential_name = dsaw.db.varchar(name="potential_name", length=64)
#    potential_name.constraints = 'PRIMARY KEY'
#    potential_name.meta['tip'] = "the unique id"


# version
__id__ = "$Id$"

# End of file 
