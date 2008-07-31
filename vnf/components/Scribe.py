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


from pyre.components.Component import Component


class Scribe(Component):

    
    def retrieveForm(self, name, director, *args):
        form = self.retrieveComponent(
            name, factory='form', args = [director] + list(args),  vault=['forms'])
        return form


    def objectEditForm(self, document, obj, properties,
                       toplevel_container, actor, director):
        '''a form to edit the given object inside the
        given actor.

        document: the UI document where the form will be inserted
        obj: the object db record to be edited
        properties: the properties of the object
        toplevel_container: the top level container db object that
            the actor is working on
        actor: the actor
        director: the director
        '''
        from ObjectEditFormCreater import ObjectEditFormCreater
        creater =  ObjectEditFormCreater()
        return creater.create(
            document, obj, properties,
            toplevel_container, actor, director)
            

# version
__id__ = "$Id: Scribe.py,v 1.27 2008-02-21 10:02:22 aivazis Exp $"

# End of file 
