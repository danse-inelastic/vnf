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

class TransientObject(Table):

    'take notes of transient objects'

    name = 'transientobjects'
    
    import dsaw.db
    
    id = dsaw.db.integer(name='id')
    id.constraints = 'PRIMARY KEY'

    target = dsaw.db.versatileReference(name='target')
    

# version
__id__ = "$Id$"

# End of file 
