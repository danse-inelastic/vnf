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


from _ import *
from vnfb.dom.Label import Label, common_labels


def select_labeled_entities_clause(name, type, db):
    '''get the labeled entities for the given label (specified by name and type)

    cols:
      entity: global address of the entity
      type: type of the entity
    '''
    sL = db._tablemap.TableToSATable(Label)
    if name in common_labels:
        whereclause="labelname='%s'" % (name,)
    else:
        whereclause="labelname='%s' and targettable='%s'" % (
            name, type)
        
    labelq = sqlalchemy.select(
        [sL.c.entity.label('entity'),
         sL.c.labelname.label('label'),
         ],
        whereclause=whereclause,
        ) .alias('labelq')

    sGP = db._tablemap.TableToSATable(global_pointer)

    q1 = sqlalchemy.select(
        [labelq.c.entity.label('entity'),
         sGP.c.type.label('type'),
         ],
        labelq.c.entity==sGP.c.id,
        )

    return q1


# version
__id__ = "$Id$"

# End of file 
