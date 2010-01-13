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


def helper(type):
    '''create a helper class for the actor class generated by orm

    type: the data object type being orm-ed
    '''

    class ShapeOrmActorHelper(object):

        def callScattererEditorActor(self, director):
            '''redirect to scatterer/editor actor

            id: id of the shape being edited
            scattererid: id of the sccatterer the scatterer editor is editing
            '''
            id = self.inventory.id
            scattererid = self.inventory.scattererid

            orm = director.clerk.orm
            table = orm(type)
            db = orm.db
            record = db.query(table).filter_by(id=self.inventory.id).one()
            uid = db.getUniqueIdentifierStr(record)

            from luban.content import load
            return load(
                actor='scatterer/editor', routine='setShape',
                id=scattererid, shape=uid
                )


        def _postStoringUserInputs(self, director):
            if hasattr(self.inventory, 'handler'):
                handler = self.inventory.handler
                handler = getattr(self, handler)
                return handler(director)
            return super(ShapeOrmActorHelper, self)._postStoringUserInputs(director)
        

    return ShapeOrmActorHelper


# version
__id__ = "$Id$"

# End of file 