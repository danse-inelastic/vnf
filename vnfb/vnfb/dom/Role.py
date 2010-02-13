#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from _ import Table


class Role(Table):
    
    
    import dsaw.db
    
    
    # the table name
    name = "roles"
    
    # the table columns
    id = dsaw.db.integer(name='id')
    id.constraints = "PRIMARY KEY"

    # name of the role, like "admin", "user", "developer"
    rolename = dsaw.db.varchar(name='rolename', length=64)
    
    # context of the role, like "mcvine", "vasp", "vnf"
    context = dsaw.db.varchar(name='context', length=64)
    
    description = dsaw.db.varchar(name="description", length=255)
    status = dsaw.db.char(name="status", length=1, default='l')
    # "l": live
    # "d": deleted


    def hasPrivilege(self, privilege, db):
        '''check if this role has the give privilege

        privilege: could be either of following two
          * a tuple of (target, name)
          * a record in the privileges table
        db: dsaw.db db manager
        '''
        
        if isinstance(privilege, tuple):
            target, name = privilege
            from Privilege import Privilege
            privilege = db.query(Privilege).filter_by(target=target, name=name).one()
        else:
            # assume privilege is already a db record of privileges table
            pass
        
        return self._hasPrivilege(privilege, db)
    

    def _hasPrivilege(self, privilege, db):
        from RoleHasPrivilege import RoleHasPrivilege
        rs = db.query(RoleHasPrivilege).filter_by(role=self.id, privilege=privilege.id).all()
        return bool(rs)
        

# version
__id__ = "$Id$"

# End of file 
