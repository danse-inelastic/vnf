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
        '''check if this user has the give role

        role: could be either of following two
          * a tuple of (context, name)
          * a record in the roles table
        db: dsaw.db db manager
        '''
        
        if isinstance(role, tuple):
            context, name = role
            from Role import Role
            role = db.query(Role).filter_by(context=context, rolename=name).one()
        else:
            # assume role is already a db record of roles table
            pass
        
        return self._hasRole(role, db)
    

    def _hasRole(self, role, db):
        from UserHasRole import UserHasRole
        rs = db.query(UserHasRole).filter_by(user=self.id, role=role.id).all()
        return bool(rs)
        

    pass # end of User



# version
__id__ = "$Id$"

# End of file 