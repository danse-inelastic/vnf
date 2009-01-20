from datetime import datetime, date, time, timedelta
from decimal import Decimal
import cPickle as pickle
import re

from vnf.exceptions import NoneError
from vnf import Undef



class LazyValue(object):
    """Marker to be used as a base class on lazily evaluated values."""
    __slots__ = ()


def raise_none_error(column):
    if not column:
        raise NoneError("None isn't acceptable as a value")
    else:
        from vnf.expr import compile, CompileError
        name = column.name
        if column.table is not Undef:
            try:
                table = compile(column.table)
                name = "%s.%s" % (table, name)
            except CompileError:
                pass
        raise NoneError("None isn't acceptable as a value for %s" % name)


def VariableFactory(cls, **old_kwargs):
    """Build cls with kwargs of constructor updated by kwargs of call.

    This is really an implementation of partial/curry functions, and
    is replaced by 'partial' when 2.5+ is in use.
    """
    def variable_factory(**new_kwargs):
        kwargs = old_kwargs.copy()
        kwargs.update(new_kwargs)
        return cls(**kwargs)
    return variable_factory

try:
    from functools import partial as VariableFactory
except ImportError:
    pass


class Variable(object):
    """Basic representation of a database value in Python.

    @type column: L{vnf.expr.Column}
    @ivar column: The column this variable represents.
    @type event: L{vnf.event.EventSystem}
    @ivar event: The event system on which to broadcast events. If
        None, no events will be emitted.
    """

    _value = Undef
    _lazy_value = Undef
    _checkpoint_state = Undef
    _allow_none = True
    _validator = None
    _validator_object_factory = None
    _validator_attribute = None

    column = None
    event = None

    def __init__(self, value=Undef, value_factory=Undef, from_db=False,
                 allow_none=True, column=None, event=None, validator=None,
                 validator_object_factory=None, validator_attribute=None):
        """
        @param value: The initial value of this variable. The default
            behavior is for the value to stay undefined until it is
            set with L{set}.
        @param value_factory: If specified, this will immediately be
            called to get the initial value.
        @param from_db: A boolean value indicating where the initial
            value comes from, if C{value} or C{value_factory} are
            specified.
        @param allow_none: A boolean indicating whether None should be
            allowed to be set as the value of this variable.
        @param validator: Validation function called whenever trying to
            set the variable to a non-db value.  The function should
            look like validator(object, attr, value), where the first and
            second arguments are the result of validator_object_factory()
            (or None, if this parameter isn't provided) and the value of
            validator_attribute, respectively.  When called, the function
            should raise an error if the value is unacceptable, or return
            the value to be used in place of the original value otherwise.
        @type column: L{vnf.expr.Column}
        @param column: The column that this variable represents. It's
            used for reporting better error messages.
        @type event: L{EventSystem}
        @param event: The event system to broadcast messages with. If
            not specified, then no events will be broadcast.
        """
        if not allow_none:
            self._allow_none = False
        if value is not Undef:
            self.set(value, from_db)
        elif value_factory is not Undef:
            self.set(value_factory(), from_db)
        if validator is not None:
            self._validator = validator
            self._validator_object_factory = validator_object_factory
            self._validator_attribute = validator_attribute
        self.column = column
        self.event = event

    def get_lazy(self, default=None):
        """Get the current L{LazyValue} without resolving its value.

        @param default: If no L{LazyValue} was previously specified,
            return this value. Defaults to None.
        """
        if self._lazy_value is Undef:
            return default
        return self._lazy_value

    def get(self, default=None, to_db=False):
        """Get the value, resolving it from a L{LazyValue} if necessary.

        If the current value is an instance of L{LazyValue}, then the
        C{resolve-lazy-value} event will be emitted, to give third
        parties the chance to resolve the lazy value to a real value.

        @param default: Returned if no value has been set.
        @param to_db: A boolean flag indicating whether this value is
            destined for the database.
        """
        if self._lazy_value is not Undef and self.event is not None:
            self.event.emit("resolve-lazy-value", self, self._lazy_value)
        value = self._value
        if value is Undef:
            return default
        if value is None:
            return None
        return self.parse_get(value, to_db)

    def set(self, value, from_db=False):
        """Set a new value.

        Generally this will be called when an attribute was set in
        Python, or data is being loaded from the database.

        If the value is different from the previous value (or it is a
        L{LazyValue}), then the C{changed} event will be emitted.

        @param value: The value to set. If this is an instance of
            L{LazyValue}, then later calls to L{get} will try to
            resolve the value.
        @param from_db: A boolean indicating whether this value has
            come from the database.
        """
        # FASTPATH This method is part of the fast path.  Be careful when
        #          changing it (try to profile any changes).

        if isinstance(value, LazyValue):
            self._lazy_value = value
            self._checkpoint_state = new_value = Undef
        else:
            if not from_db and self._validator is not None:
                # We use a factory rather than the object itself to prevent
                # the cycle object => obj_info => variable => object
                value = self._validator(self._validator_object_factory and
                                        self._validator_object_factory(),
                                        self._validator_attribute, value)
            self._lazy_value = Undef
            if value is None:
                if self._allow_none is False:
                    raise_none_error(self.column)
                new_value = None
            else:
                new_value = self.parse_set(value, from_db)
                if from_db:
                    # Prepare it for being used by the hook below.
                    value = self.parse_get(new_value, False)
        old_value = self._value
        self._value = new_value
        if (self.event is not None and
            (self._lazy_value is not Undef or new_value != old_value)):
            if old_value is not None and old_value is not Undef:
                old_value = self.parse_get(old_value, False)
            self.event.emit("changed", self, old_value, value, from_db)

    def delete(self):
        """Delete the internal value.

        If there was a value set, then emit the C{changed} event.
        """
        old_value = self._value
        if old_value is not Undef:
            self._value = Undef
            if self.event is not None:
                if old_value is not None and old_value is not Undef:
                    old_value = self.parse_get(old_value, False)
                self.event.emit("changed", self, old_value, Undef, False)

    def is_defined(self):
        """Check whether there is currently a value.

        @return: boolean indicating whether there is currently a value
            for this variable. Note that if a L{LazyValue} was
            previously set, this returns False; it only returns True if
            there is currently a real value set.
        """
        return self._value is not Undef

    def has_changed(self):
        """Check whether the value has changed.

        @return: boolean indicating whether the value has changed
            since the last call to L{checkpoint}.
        """
        return (self._lazy_value is not Undef or
                self.get_state() != self._checkpoint_state)

    def get_state(self):
        """Get the internal state of this object.

        @return: A value which can later be passed to L{set_state}.
        """
        return (self._lazy_value, self._value)

    def set_state(self, state):
        """Set the internal state of this object.

        @param state: A result from a previous call to
            L{get_state}. The internal state of this variable will be set
            to the state of the variable which get_state was called on.
        """
        self._lazy_value, self._value = state

    def checkpoint(self):
        """"Checkpoint" the internal state.

        See L{has_changed}.
        """
        self._checkpoint_state = self.get_state()

    def copy(self):
        """Make a new copy of this Variable with the same internal state."""
        variable = self.__class__.__new__(self.__class__)
        variable.set_state(self.get_state())
        return variable

    def parse_get(self, value, to_db):
        """Convert the internal value to an external value.

        Get a representation of this value either for Python or for
        the database. This method is only intended to be overridden
        in subclasses, not called from external code.

        @param value: The value to be converted.
        @param to_db: Whether or not this value is destined for the
            database.
        """
        return value

    def parse_set(self, value, from_db):
        """Convert an external value to an internal value.

        A value is being set either from Python code or from the
        database. Parse it into its internal representation.  This
        method is only intended to be overridden in subclasses, not
        called from external code.

        @param value: The value, either from Python code setting an
            attribute or from a column in a database.
        @param from_db: A boolean flag indicating whether this value
            is from the database.
        """
        return value
