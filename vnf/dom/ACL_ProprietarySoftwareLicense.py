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


# role-(proprietary software license) relation


from ACL_Privilege import ACL_Privilege as base


class ACL_ProprietarySoftwareLicense(base):

    name = "acl_proprietarysoftwarelicenses"
    
    import pyre.db
    
    id = pyre.db.varchar(name="id", length=64)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    role = pyre.db.varchar(name='role', length=64)
    role.constraints = 'REFERENCES roles (id)'

    name = pyre.db.varchar(name='name', length=64)
    name.meta['tip'] = 'Software name'
    
    pass # end of ACL_ProprietarySoftwareLicense


# version
__id__ = "$Id$"

# End of file 
