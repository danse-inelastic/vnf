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

    class KernelOrmActorHelper(object):


        def callScattererEditorActor(self, director):
            '''redirect to scatterer/editor actor

            id: id of the kernel being edited
            scattererid: id of the sccatterer the scatterer editor is editing
            oldkerneluid: unique identifier of the kernel that was in the
              kernel list of the scatterer.
            '''
            id = self.inventory.id
            scattererid = self.inventory.scattererid
            oldkerneluid = self.inventory.oldkerneluid

            orm = director.clerk.orm
            table = orm(type)
            db = orm.db
            record = db.query(table).filter_by(id=self.inventory.id).one()
            uid = db.getUniqueIdentifierStr(record)
            from luban.content import load
            return load(
                actor='scatterer/editor', routine='setKernel',
                id=scattererid, oldkernel=oldkerneluid, kernel=uid
                )


        def _postStoringUserInputs(self, director):
            if hasattr(self.inventory, 'handler'):
                handler = self.inventory.handler
                handler = getattr(self, handler)
                return handler(director)
            return super(KernelOrmActorHelper, self)._postStoringUserInputs(director)



    # drawer helpers
        

    return KernelOrmActorHelper


# version
__id__ = "$Id$"

# End of file 