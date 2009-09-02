from vnf import Undef

from vnf.utils.expr import Expr, FromExpr, Column, Desc, TABLE
from vnf.utils.expr import SQLToken, CompileError, compile

def get_obj_info(obj):
    try:
        return obj.__storm_object_info__
    except AttributeError:
        # Instantiate ObjectInfo first, so that it breaks gracefully,
        # in case the object isn't a storm object.
        obj_info = ObjectInfo(obj)
        return obj.__dict__.setdefault("__storm_object_info__", obj_info)

def set_obj_info(obj, obj_info):
    obj.__dict__["__storm_object_info__"] = obj_info

def get_cls_info(cls):
    if "__storm_class_info__" in cls.__dict__:
        # Can't use attribute access here, otherwise subclassing won't work.
        return cls.__dict__["__storm_class_info__"]
    else:
        cls.__storm_class_info__ = ClassInfo(cls)
        return cls.__storm_class_info__

class ClassInfo(dict):
    """Persistent storm-related information of a class.

    The following attributes are defined:

    @ivar table: Expression from where columns will be looked up.
    @ivar cls: Class which should be used to build objects.
    @ivar columns: Tuple of column properties found in the class.
    @ivar primary_key: Tuple of column properties used to form the primary key
    @ivar primary_key_pos: Position of primary_key items in the columns tuple.
    """

    def __init__(self, cls):
        self.table = getattr(cls, "__storm_table__", None)
        if self.table is None:
            raise Exception("%sClassInfoError.__storm_table__ missing" % repr(cls))

        self.cls = cls

        if isinstance(self.table, basestring):
            self.table = SQLToken(self.table)

        pairs = []
        for attr in dir(cls):
            column = getattr(cls, attr, None)
            if isinstance(column, Column):
                pairs.append((attr, column))


        pairs.sort()

        self.columns = tuple(pair[1] for pair in pairs)
        self.attributes = dict(pairs)

        storm_primary = getattr(cls, "__storm_primary__", None)
        if storm_primary is not None:
            if type(storm_primary) is not tuple:
                storm_primary = (storm_primary,)
            self.primary_key = tuple(self.attributes[attr]
                                     for attr in storm_primary)
        else:
            primary = []
            primary_attrs = {}
            for attr, column in pairs:
                if column.primary != 0:
                    if column.primary in primary_attrs:
                        raise Exception(
                            "%s has two columns with the same primary id: "
                            "%s and %s" %
                            (repr(cls), attr, primary_attrs[column.primary]))
                    primary.append((column.primary, column))
                    primary_attrs[column.primary] = attr
            primary.sort()
            self.primary_key = tuple(column for i, column in primary)

        if not self.primary_key:
            raise Exception("%s has no primary key information" %
                                 repr(cls))

        # columns have __eq__ implementations that do things we don't want - we
        # want to look these up in a dict and use identity semantics
        id_positions = dict((id(column), i)
                             for i, column in enumerate(self.columns))

        self.primary_key_idx = dict((id(column), i)
                                    for i, column in
                                    enumerate(self.primary_key))
        self.primary_key_pos = tuple(id_positions[id(column)]
                                     for column in self.primary_key)


        __order__ = getattr(cls, "__storm_order__", None)
        if __order__ is None:
            self.default_order = Undef
        else:
            if type(__order__) is not tuple:
                __order__ = (__order__,)
            self.default_order = []
            for item in __order__:
                if isinstance(item, basestring):
                    if item.startswith("-"):
                        prop = Desc(getattr(cls, item[1:]))
                    else:
                        prop = getattr(cls, item)
                else:
                    prop = item
                self.default_order.append(prop)

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return self is not other