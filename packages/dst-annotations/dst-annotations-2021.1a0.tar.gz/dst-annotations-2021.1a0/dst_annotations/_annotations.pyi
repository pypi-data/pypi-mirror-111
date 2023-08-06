import dataclasses
import inspect
from typing import (
    Any,
    ClassVar,
    Dict,
    Literal,
    Protocol,
    Tuple,
    Type,
    Union,
    runtime_checkable,
)


class _MissingType(Protocol):

    @classmethod
    def __subclasshook__(cls, other):
        return other is type(dataclasses.MISSING)


@runtime_checkable
class _DClsOrObj(Protocol):
    __dataclass_fields__: Dict[str, dataclasses.Field]


@runtime_checkable
class AnnotatedAlias(Protocol):
    __args__: Tuple[Any]
    __metadata__: Tuple


class Empty:
    ...


GenericAlias: Type = ...
TEmpty = Union[Type[inspect.Parameter.empty], Empty, _MissingType]

empty: Empty = ...


@runtime_checkable
class NamedTupleProto(Protocol):
    __annotations__: Dict[str, Any]
    _fields: ClassVar[Tuple[str, ...]]
    _field_defaults: ClassVar[Dict[str, Any]]
    _field_types: ClassVar[Dict[str, Any]]


@runtime_checkable
class DataClassProto(Protocol):
    __annotations__: Dict[str, Any]
    __dataclass_fields__: ClassVar[Dict[str, dataclasses.Field]]


@runtime_checkable
class ValidDataClassProto(DataClassProto, Protocol):

    @classmethod
    def __subclasshook__(cls, subclass):
        if not isinstance(subclass, _DClsOrObj):
            return False
        for f in subclass.__dataclass_fields__.values():
            if f.type is dataclasses.InitVar and f.default is dataclasses.MISSING:
                return False
        return True


@runtime_checkable
class AnnotatedClassProto(Protocol):
    __annotations__: Dict[str, Any]
    __is_annotated__: ClassVar[Literal[True]]


@runtime_checkable
class TypedDictProto(Protocol):
    __annotations__: Dict[str, Any]
    __total__: ClassVar[bool]


NamedClassProto = Union[TypedDictProto, NamedTupleProto, ValidDataClassProto, AnnotatedClassProto]


@runtime_checkable
class ForwardRefProto(Protocol):
    __forward_arg__: str
