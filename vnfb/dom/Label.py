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

'''
This table gives users a way to label his data objects (records).

fields:
 creator: 
 date:
 labelname: name of the label
 entity: the entity (db record) this label is about
 targettable: some labels are specific to a table (view). this
    property gives the name of the table (view).

Note
* When entity is empty, a label record represents a label without 
  target. This is useful for getting all the names of labels, for
  example.
* There are labels for common purpose. See common_labels.
'''


from OwnedObject import OwnedObject as base
class Label(base):

    name = 'labels'

    import dsaw.db
    
    labelname = dsaw.db.varchar(name='labelname', length=64)
    entity = dsaw.db.versatileReference(name = 'entity')
    targettable = dsaw.db.varchar(name='targettable', length=64)


common_labels = ['private']


# version
__id__ = "$Id$"

# End of file 
