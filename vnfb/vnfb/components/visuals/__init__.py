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

from luban.content import select, load, alert
import luban.content as lc


def set_contextual_help(page='', label=''):
    actions = []
    changepage = select(id='help-page-text').setAttr(value=page)
    actions.append(changepage)
    
    if label:
        changelabel = select(id='help-portlet-about-context').setAttr(label=label)
        actions.append(changelabel)
        
    return actions


class VisualFactory(object):

    def __call__(self, *args, **kwds):
        raise NotImplementedError


class VisualFactory_withAcessControl(VisualFactory):


    def create(self, **kwds):
        raise NotImplementedError


    def checkPrivilege(self):
        raise NotImplementedError


    def __call__(self, *args, **kwds):
        # there might be one argument that is the director
        if len(args) > 1:
            raise ValueError, "args: %s, kwds: %s" % (args, kwds)
        if len(args):
            kwds['director'] = args[0]
        #
        director = kwds['director']
        self.director = director
        if self.checkPrivilege():
            return lc.document(title='not enough privilege')

        return self.create(**kwds)


class VisualFactory_withPrivilegeRequirement(VisualFactory_withAcessControl):

    # required
    privilege = None

    def checkPrivilege(self):
        director = self.director
        username = director.sentry.username
        user = director.clerk.getUser(username)
        privilege = self.privilege
        db = director.clerk.db
        return not user.hasPrivilege(privilege, db)


# version
__id__ = "$Id$"

# End of file 
