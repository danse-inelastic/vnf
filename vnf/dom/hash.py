# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



#__builtin_hash = __builtins__['hash']


def hash(obj, db):
    hasher = Hasher()
    return hasher.hash(obj, db)


from pyre.db.Table import Table
class Hasher:

    def __init__(self):
        self.level = 0
        self.rooms = {} # room number for each level
        self._addressbook = {}
        return
    

    def hash(self, obj, db=None):
        #print self._addressbook
        if self._id(obj) in self._addressbook:
            return self._addressbook[self._id(obj)]
        
        handler = self._getHandler(obj.__class__)
        self.level += 1
        if self.rooms.get(self.level) is None:
            self.rooms[self.level] = 0
        self._addressbook[self._id(obj)] = str( (self._address(), obj.__class__.__name__) )
        ret = handler(obj, db=db)
        self.level -= 1
        return ret


    def hash_dbrecord(self, record, db):
        'create a hash value from a db record'
        # the difficulty of hashing a db record is that it may contain references
        # so we need to hash recursively
        Table = record.__class__
        d = []
        for attrname in dir(Table):
            attr = getattr(Table, attrname)
            if not isDescriptor(attr): continue

            name = attr.name
            # skip id
            if name == 'id': continue

            if isReference(attr):
                ref = attr.__get__(record)
                #print 'ref=', ref
                if ref:
                    value = ref.dereference(db)
                else:
                    value = ''
                #print 'value=', value
            else:
                # !!! should define hashers for different types. this is a quick hack
                value = str(attr.__get__(record))

            d.append('(%s, %s)' % (name, self.hash(value, db)) )

        s = '%s%s' % (Table.name, ','.join(d))
        return s


    def hash_tuple(self, t, db=None):
        hashes = []
        for i, e in enumerate(t):
            self.rooms[self.level] += 1
            hashes.append(self.hash(e,db))
            continue
        return '(' + ','.join(hashes) + ')'

    hash_list = hash_tuple

    def hash_dict(self, d, db=None):
        t = [ (k,v) for k,v in d.iteritems() ]
        return self.hash_list(t, db)

    def hash_str(self, s, db=None):
        return s


    _hashers = {
        tuple: 'hash_tuple',
        dict: 'hash_dict',
        list: 'hash_list',
        str: 'hash_str',
        Table: 'hash_dbrecord',
        }
    def _getHandler(self, type):
        if issubclass(type, Table): type=Table
        return getattr(self, self._hashers[type])


    def _address(self):
        return self.level, self.rooms[self.level]


    def _id(self, obj):
        # return a unique id for an object
        # for a normal object, id(obj) will do the work
        # for a db record, we need (table name, id) tuple
        if isinstance(obj, Table):
            return '%s:%s' % (obj.name, obj.id)
        return id(obj)



from pyre.db.Column import Column
Descriptors = [
    Column,
    ]

from ReferenceSet import ReferenceSet
Descriptors.append(ReferenceSet)
from Geometer import Geometer
Descriptors.append(Geometer)

def isDescriptor(candidate):
    for Descriptor in Descriptors:
        if isinstance(candidate, Descriptor):
            return True
        continue
    return False


from pyre.db.Reference import Reference
from pyre.db.VersatileReference import VersatileReference
from ReferenceSet import ReferenceSet
from Geometer import Geometer
References = [
    Reference,
    VersatileReference,
    ReferenceSet,
    Geometer,
    ]

def isReference(candidate):
    for R in References:
        if isinstance(candidate, R):
            return True
        continue
    return False


# version
__id__ = "$Id$"

# End of file 
