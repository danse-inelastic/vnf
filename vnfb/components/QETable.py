#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

"""
QETable - abstract class for all QE database tables. It serves as an adapter for
VNF Clerk for convenience purposes (in case if interfaces change)

Notes on database classes implementation:
1. All the tables inherited from QETable have 'id' column!
2. There are two alternative ways to perform action (update, create, delete) on database class:
    - Directly use clerk's methods (e.g. Clerk.updateRecord(record)) by passing the class object
        Pros: Saves extra call
        Cons: Not very convenient to write
    - Use QETable methods (e.g. QETable.updateRecord(params) by passing dictionary of parameters
      (e.g. params = {"id": 5, "name": "Hi", ...})
      Pros: Convenient for handling table forms?
3. Using QETable methods does not require passing director every time you use it.
"""

from vnfb.qeutils.qeutils import timestamp, newid, setname, ifelse
from dsaw.db.WithID import WithID
#from vnfb.dom.Computation import Computation

NO_UPDATE   = ["timecreated", "date", "id"]
STAMPED     = ["timecreated", "timemodified"]
DATED       = ["date",]

class QETable(WithID):

    def __init__(self, director = None):
        super(QETable, self).__init__()
        self._director      = director
        if director:
            self._clerk     = director.clerk
        else:
            self._clerk     = None


    def setClerk(self, clerk):
        self._clerk = clerk


    def setDirector(self, director):
        self._director  = director
        self._clerk     = director.clerk    # Specific for director


    # Haven't tested yet
    def updateRecord(self, params):
        """Tries to update record, otherwise complains"""
        for column in self.getColumnNames():
            if self._noUpdate(column):  # Do not updated values
                continue

            if self._stamp(column):     # Time is updated either to user specified value or to timestamp
                setattr(self, column, ifelse(params.get(column), params.get(column), timestamp()))
                continue

            setattr(self, column, setname(params, self, column))

        try:
            self._clerk.updateRecordWithID(self)   # Commit to database
        except:
            raise   # Complain


    def createRecord(self, params):
        """Tries to create record, otherwise complains"""
        for column in self.getColumnNames():
            if self._date(column):
                continue    # Creates automatically?


            if self._id(column):
                setattr(self, column, ifelse(params.get(column), params.get(column), newid(self._director)))
                continue

            if self._stamp(column):
                setattr(self, column, ifelse(params.get(column), params.get(column), timestamp()))
                continue

            setattr(self, column, setname(params, self, column))

        try:
            self._clerk.insertNewRecord(self)
        except:
            raise   # Complain

#    @classmethod
#    def getActorName(cls):
#        if hasattr(cls, 'actor'): return cls.actor
#        return cls.__name__.lower()


    # Haven't tested yet
    def deleteRecord(self):
        """Deletes record is clerk exists, ignores otherwise"""
        if self._clerk:
            self._clerk.deleteRecordWithID(self)    # , where="id='%s'" % getattr(self, 'id')


    def _noUpdate(self, value):
        """Value that should not be updated"""
        if value in NO_UPDATE:
            return True

        return False

    def _stamp(self, value):
        """Value that should be time stamped"""
        if value in STAMPED:
            return True

        return False

    def _id(self, value):
        if value == 'id':
            return True

        return False

    def _date(self, value):
        """Value that should be time stamped"""
        if value in DATED:
            return True

        return False

__date__ = "$Nov 24, 2009 5:52:44 PM$"


