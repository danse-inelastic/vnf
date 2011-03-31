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


from vnf.dom.Label import Label, common_labels
def select_public_and_owned_records(cols, table, username, db):
    '''
    cols must be columns of the given table.
    table must have the following columns
      * globalpointer
      * creator
    table must have a name. if it is a query itself, alias it.
    '''
    sL = db._tablemap.TableToSATable(Label)
    qL = sqlalchemy.select(
        [sL.c.entity], 
        whereclause=sL.c.labelname=='private',
        ).alias('privatelabelq')
    onclause = table.c.globalpointer == qL.c.entity
    cols2 = [qL.c.entity]
    q1 = sqlalchemy.select(
        cols+cols2,
        from_obj=[table.outerjoin(qL, onclause=onclause)],
        )
            
    where = "creator is NULL OR creator='%s' OR creator!='%s' AND entity IS NULL" % (username, username)
    q = sqlalchemy.select(
        [q1.alias('privatelabeloj')], 
        whereclause = where,
        )
    return q


# version
__id__ = "$Id$"

# End of file 
