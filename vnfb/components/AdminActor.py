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


from luban.content import load, select, alert
class AdminActorAddOn(object):

    privilege = ('system', 'administrate')


    def perform(self, director, **kwds):
        if self._checkPrivilege(director):
            return alert("You don't have enough privilege")
        return super(AdminActorAddOn, self).perform(director, **kwds)


    def _checkPrivilege(self, director):
        username = director.sentry.username
        user = director.clerk.getUser(username)
        privilege = self.privilege
        db = director.clerk.db
        return not user.hasPrivilege(privilege, db)



from AuthorizedActor import AuthorizedActor as base, portal
class AdminActor(AdminActorAddOn, base):

    pass


from luban.components.Actor import AcceptArbitraryInput
class AdminReceptionist(AcceptArbitraryInput, AdminActor):
    
    pass


from luban.components.FormProcessor import FormProcessor
class AdminFormProcessor(AdminActorAddOn, FormProcessor):
    
    pass


# version
__id__ = "$Id$"

# End of file 
