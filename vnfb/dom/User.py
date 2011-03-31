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


from _ import Table as base


class User(base):

    name = "users"
    
    import dsaw.db
    
    id = dsaw.db.varchar(name="id", length=64)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    username = dsaw.db.varchar(name="username", length=64)
    username.meta['tip'] = "the user's name"
    #username.constraints = "PRIMARY KEY"
    
    password = dsaw.db.varchar(name="password", length=64)
    password.meta['tip'] = "the user's password"

    fullname = dsaw.db.varchar(name='fullname', length=1024)

    email = dsaw.db.varchar(name='email', length=128)


    def __str__(self):
        return 'user(name=%s)' % self.username


    def hasRole(self, role, db):
        '''check (recursively) if this user has the given role
        '''
        # convert role to db record
        if isinstance(role, tuple):
            role = self._getRole(role, db)
            
        # if I have this role directly, then good
        if self._hasRoleDirectly(role, db): return True
        
        # else, find all my groups, and ask the group if he has the given role
        for group in self._directRoles(db):
            if group.hasRole(role, db): return True
            continue
        return False


    def assignRole(self, role, db):
        '''assign the given role to me'''
        from UserHasRole import assign
        return assign(role, self, db)


    def join(self, group, db):
        '''join a gropu (role). this is just an alias of "assignRole"
        '''
        return self.assignRole(group, db)


    def hasPrivilege(self, privilege, db):
        '''check if the user has the given privilege

        user: db record in users table
        privilege: either of following two
          1. a tuple of (target, name)
          2. a record in the privileges table

        '''
        # the implementation here first find all the roles that
        # has the given privilege, then test if the user has
        # one of the roles.
        privilege = self._getPrivilege(privilege, db)

        # in the future, when role_has_roles is created, we
        # need a recursion algorithm
        roles = privilege.findRoles(db)

        for role in roles:
            if self.hasRole(role, db): return True
            continue
        return False


    def _getPrivilege(self, privilege, db):
        target, name = privilege
        from vnfb.dom.Privilege import Privilege
        privilege = db.query(Privilege).filter_by(target=target, name=name).one()
        return privilege
    

    def _directRoles(self, db):
        'list all my direct roles'
        records = self._queryUserHasRole(db).filter_by(user=self.id).all()
        roles = [r.role.dereference(db) for r in records]
        return roles
    

    def _hasRoleDirectly(self, role, db):
        '''check if this user has the give role

        role: could be either of following two
          * a tuple of (context, name)
          * a record in the roles table
        db: dsaw.db db manager
        '''
        return bool(self._hasRoleQuery(role, db).all())


    def _getRole(self, role, db):
        context, name = role
        from Role import Role
        role = db.query(Role).filter_by(context=context, rolename=name).one()
        return role
    

    def _queryUserHasRole(self, db):
        from UserHasRole import UserHasRole
        return db.query(UserHasRole)


    def _hasRoleQuery(self, role, db):
        q = self._queryUserHasRole(db)
        return q.filter_by(user=self.id, role=role.id)
        

    pass # end of User



# version
__id__ = "$Id$"

# End of file 
