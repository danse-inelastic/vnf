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


from vnf.applications.WebApplication import AuthenticationError
from vnf.content import action, actionRequireAuthentication
from vnf.weaver import action_link



from opal.components.Actor import Actor as base
class Actor(base):


    def nyi(self, director):
        """notify the user that the requested routine is not yet implemented"""
        page = director.retrievePage("nyi")
        main = page._body._content._main
        document = main.document(title = 'Under construction...')
        p = document.paragraph()
        p.text = [
            "Not implemented yet! actor=%s, routine=%s" % (
            self.name, director.inventory.routine),
            ]
        return page

    pass


# version
__id__ = "$Id$"

# End of file 
