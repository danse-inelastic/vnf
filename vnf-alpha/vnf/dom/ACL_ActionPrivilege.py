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


# role-(action privilege) relation


from ACL_Privilege import ACL_Privilege as base


class ACL_ActionPrivilege(base):

    name = "acl_actionprivileges"
    
    import dsaw.db
    
    id = dsaw.db.varchar(name="id", length=64)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    role = dsaw.db.varchar(name='role', length=64)
    role.constraints = 'REFERENCES roles (id)'

    action = dsaw.db.varchar(name='action', length=64)
    routine = dsaw.db.varchar(name='routine', length=64)
    
    pass # end of ACL_ActionPrivilege


# version
__id__ = "$Id$"

# End of file 
