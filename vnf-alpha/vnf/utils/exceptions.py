#
# Copyright (c) 2006, 2007 Canonical
#
# Written by Gustavo Niemeyer <gustavo@niemeyer.net>
#
# This file is part of Storm Object Relational Mapper.
#
# Storm is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of
# the License, or (at your option) any later version.
#
# Storm is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


class VnfError(Exception):
    pass


class CompileError(VnfError):
    pass

class NoTableError(CompileError):
    pass

class ExprError(VnfError):
    pass

class NoneError(VnfError):
    pass

class PropertyPathError(VnfError):
    pass

class ClassInfoError(VnfError):
    pass


class URIError(VnfError):
    pass


class ClosedError(VnfError):
    pass

class FeatureError(VnfError):
    pass

class DatabaseModuleError(VnfError):
    pass


class StoreError(VnfError):
    pass

class NoStoreError(VnfError):
    pass

class WrongStoreError(StoreError):
    pass

class NotFlushedError(StoreError):
    pass

class OrderLoopError(StoreError):
    pass

class NotOneError(StoreError):
    pass

class UnorderedError(StoreError):
    pass

class LostObjectError(StoreError):
    pass


class Error(VnfError):
    pass

class Warning(VnfError):
    pass

class InterfaceError(Error):
    pass

class DatabaseError(Error):
    pass

class InternalError(DatabaseError):
    pass

class OperationalError(DatabaseError):
    pass

class ProgrammingError(DatabaseError):
    pass

class IntegrityError(DatabaseError):
    pass

class DataError(DatabaseError):
    pass

class NotSupportedError(DatabaseError):
    pass


class DisconnectionError(OperationalError):
    pass

class TimeoutError(VnfError):
    """Raised by timeout tracers when remining time is over."""

    def __init__(self, statement, params):
        self.statement = statement
        self.params = params

    def __str__(self):
        return "%r, %r" % (self.statement, self.params)


def install_exceptions(module):
    for exception in (Error, Warning, DatabaseError, InternalError,
                      OperationalError, ProgrammingError, IntegrityError,
                      DataError, NotSupportedError):
        module_exception = getattr(module, exception.__name__, None)
        if module_exception is not None:
            module_exception.__bases__ += (exception,)
