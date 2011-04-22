# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2007-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# mixin class to support master table view creation
# for one single db table.


from DOMAccessorMixinForMasterTable import DOMAccessorMixinForMasterTable as base, sqlalchemy
class DOMAccessorMixinForMasterTable_SingleTable(base):

    Table = None # the single table to query. a subclass of dsaw.db.Table
    columns = [] # names of cols of interests

    def customizeFilter(self, filter):
        # reload this to provide customization
        return filter
    

    def makeQuery(self, filter=None, label=None, mine=False):
        if label:
            if filter: raise RuntimeError
            return self.makeLabeledQuery(label, mine=mine)
        db = self.db

        # query
        st = db._tablemap.TableToSATable(self.Table)
        cols = [getattr(st.c, col) for col in self.columns]
        username = self.getUsername()
        if mine:
            q = sqlalchemy.select(cols, st.c.creator==username)
        else:
            from vnf.utils.query.accesscontrol import select_public_or_owned_records
            q = select_public_or_owned_records(cols, st, username, db)

        filter = self.customizeFilter(filter)
        # filter query
        if filter:
            q = sqlalchemy.select([q.alias('tofilter')], whereclause=filter)
        return q


    def makeLabeledQuery(self, label, mine=False):
        db = self.db
        sL = db._tablemap.TableToSATable(Label)
        if label in common_labels:
            whereclause="labelname='%s'" % (label,)
        else:
            whereclause="labelname='%s' and targettable='%s'" % (
                label, tablename)
        labelq = sqlalchemy.select(
            [sL.c.entity.label('entity'),
             sL.c.labelname.label('label'),
             ],
            whereclause=whereclause,
            ).alias('labelq')
        
        st = db._tablemap.TableToSATable(self.Table)
        
        cols = [getattr(st.c, col) for col in self.columns]
        cols.append(labelq.c.entity.label('gptr'))
        # where = st.c.globalpointer==labelq.c.entity
        where = 'globalpointer=labelq.entity'
        if mine:
            username = self.getUsername()
            mine = "creator='%s'" % username
            where = '%s and %s' % (where, mine)
        q = sqlalchemy.select(cols, where)
        
        return q


# End of file 
