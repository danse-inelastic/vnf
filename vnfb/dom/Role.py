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


    def becomeMember(self, group, db):
        from RoleHasRole import join
        return join(self, group, db)


    def hasRole(self, role, db):
        # if I have this role directly, then good
        if self._hasRoleDirectly(role, db): return True
        # else, find all my groups, and ask the group if he has the given role
        for group in self._directGroups(db):
            if group.hasRole(role, db): return True
            continue
        return False


    def hasPrivilege(self, privilege, db):
        '''check if this role has the given privilege

        privilege: could be either of following two
          * a tuple of (target, name)
          * a record in the privileges table
        db: dsaw.db db manager
        '''
        # if I have this privilege directly, then good
        if self._hasPrivilegeDirectly(privilege, db): return True
        # else, find all my groups, and ask the group if it has the given privilege
        for group in self._directGroups(db):
            if group.hasPrivilege(privilege, db): return True
            continue
        return False


    def _hasPrivilegeDirectly(self, privilege, db):
        '''check if this role has the given privilege directly

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
        
        return bool(self._hasPrivilegeQuery(privilege, db).all())
    

    def _directGroups(self, db):
        'list all my direct groups'
        records = self._queryRoleHasRole(db).filter_by(member=self.id).all()
        groups = [r.group.dereference(db) for r in records]
        return groups
    

    def _hasRoleDirectly(self, role, db):
        '''check if this role has the give role

        role: could be either of following two
          * a tuple of (context, name)
          * a record in the roles table
        db: dsaw.db db manager
        '''
        if isinstance(role, tuple):
            context, name = role
            role = db.query(Role).filter_by(context=context, rolename=name).one()
        else:
            # assume role is already a db record of roles table
            pass
        
        return bool(self._hasRoleQuery(role, db).all())


    def _queryRoleHasPrivilege(self, db):
        from RoleHasPrivilege import RoleHasPrivilege
        return db.query(RoleHasPrivilege)


    def _hasPrivilegeQuery(self, privilege, db):
        q = self._queryRoleHasPrivilege(db)
        return q.filter_by(role=self.id, privilege=privilege.id)


    def _queryRoleHasRole(self, db):
        from RoleHasRole import RoleHasRole
        return db.query(RoleHasRole)


    def _hasRoleQuery(self, role, db):
        q = self._queryRoleHasRole(db)
        return q.filter_by(member=self.id, group=role.id)


    def join(self, group, db):
        'join the given group'
        from RoleHasRole import join
        return join(self, group, db)
        

# version
__id__ = "$Id$"

# End of file 
