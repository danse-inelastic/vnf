# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def hasPrivilege(user, target=None, name=None, db=None):
    '''check if the user has the given privilege

    user: db record in users table (or user id)
    target: target of the privilege. see Privilege class for more details
    name: name of the privilege. see Privilege class for more details
    db: db connection
    '''
    from vnfb.dom.User import User
    if not isinstance(user, User):
        user = db.query(User).filter_by(id=user).one()
        
    return user.hasPrivilege((target,name), db)


# version
__id__ = "$Id$"

# End of file 
