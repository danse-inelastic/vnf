# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class ActorAddOn(object):


    def _getRegistrantRecords(self, username, director):
        from vnf.dom.Registrant import Registrant as Table
        return director.clerk.db.query(Table).filter_by(username=username).all()


    def _getUserRecords(self, username, director):
        from vnf.dom.User import User as Table
        return director.clerk.db.query(Table).filter_by(username=username).all()



def createKey(registrant):
    firstname = registrant.firstname
    lastname = registrant.lastname
    organization = registrant.organization
    s = '%s-%s-%s' % (firstname, lastname, organization)
    import hashlib
    return hashlib.md5(s).hexdigest()


# version
__id__ = "$Id: __init__.py 3677 2011-03-31 22:12:33Z linjiao $"

# End of file 
