# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from OwnedObject import OwnedObject as base
class Label(base):

    name = 'labels'

    import dsaw.db
    
    labelname = dsaw.db.varchar(name='labelname', length=64)
    entity = dsaw.db.versatileReference(name = 'entity')
    targettable = dsaw.db.varchar(name='targettable', length=64)


# version
__id__ = "$Id$"

# End of file 
