# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from AbstractOwnedObjectBase import AbstractOwnedObjectBase as base

class Bug(base):

    pyredbtablename = 'bugs'

    import dsaw.db
    
    traceback = dsaw.db.varchar(name='traceback', length=100000)
    comment = dsaw.db.varchar(name='comment', length=1024)



# version
__id__ = "$Id$"

# End of file 
