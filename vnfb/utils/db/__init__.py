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


def destroy(record, domaccess, username):
    if hasattr(record, 'creator') and record.creator != username:
        raise RuntimeError, "Cannot destory because you are not owner. You: %s, record owner: %s" % (username, record.creator)
    
    from findreferrals import hasreferral
    if hasreferral(record, domaccess):
        raise RuntimeError, "%s:%s still in use" % (
            record.__class__.__name__, record.id)

    orm = domaccess.orm
    obj = orm.record2object(record)
    orm.destroy(obj)
    return


# version
__id__ = "$Id$"

# End of file 
