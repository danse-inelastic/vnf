# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2007-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# mixin class to support master table view creation
# for db table(s).
# this is a base class
# see DOMAccessorMixinForMasterTable_... classes


class DOMAccessorMixinForMasterTable(object):

    db = None # db manager

    def getRecord(self, id):
        raise NotImplementedError
    

    def getUsername(self):
        "get username"
        return self.director.sentry.username
    

    def countRecords(self, filter=None, label=None, mine=False):
        q = self.makeQuery(filter=filter, label=label, mine=mine)
        return q.alias('tocount').count().execute().fetchone()[0]
    
    
    def getIDs(
        self,
        filter=None, order_by=None, reverse_order=None, slice=None,
        label=None,
        mine=False,
        ):
        
        db = self.db
        q = self.makeQuery(filter=filter, label=label, mine=mine)

        if order_by:
            q = q.order_by(order_by)
        if slice:
            if reverse_order:
                n = self.countRecords(filter=filter, label=label, mine=mine)
                slice = n-slice[1], n-slice[0]
            q = sqlalchemy.select(
                [q.alias('toslice')],
                limit = slice[1]-slice[0],
                offset = slice[0])

        ret = q.execute().fetchall()
        
        if reverse_order:
            ret.reverse()
        return [i.id for i in ret]


    def getRecords(
        self,
        filter=None, order_by=None, reverse_order=None, slice=None,
        label=None,
        mine=False,
        ):
        ids = self.getIDs(
            filter=filter, 
            order_by=order_by, reverse_order=reverse_order, 
            slice=slice,
            label=label, mine=mine,
            )
        return map(self.getRecord, ids)


import sqlalchemy

# End of file 
