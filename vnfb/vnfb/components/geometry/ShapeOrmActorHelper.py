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

    class ShapeOrmActorHelper(object):

        def _postStoringUserInputs(self, director):
            orm = director.clerk.orm
            table = orm(type)
            db = orm.db
            record = db.query(table).filter_by(id=self.inventory.id).one()
            return db.getUniqueIdentifierStr(record)

    return ShapeOrmActorHelper


# version
__id__ = "$Id$"

# End of file 
