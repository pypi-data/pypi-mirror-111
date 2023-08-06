import inspect
import typing
from abc import ABCMeta
from dataclasses import (
    MISSING,
    InitVar,
    is_dataclass,
)
from typing import (
    List,
    Protocol,
    Type,
    TypedDict,
    Union,
    runtime_checkable,
)

import typing_extensions
from typing_extensions import Annotated

GenericAlias = type(List)
assert getattr(typing, "_GenericAlias") is GenericAlias

AnnotatedAlias = type(Annotated[str, ""])
assert getattr(typing_extensions, "_AnnotatedAlias") is AnnotatedAlias


class Empty:

    def __repr__(self):
        return "<empty>"


TEmpty = Union[Type[inspect.Parameter.empty], Empty, type(MISSING)]

empty = Empty()


def _is_annotated_class(subclass):
    return isinstance(subclass, type) and isinstance(getattr(subclass, "__annotations__", None), dict)


class NamedTupleProto(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return _is_annotated_class(subclass) and issubclass(subclass, tuple) and hasattr(subclass, "_fields")


class DataClassProto(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return _is_annotated_class(subclass) and is_dataclass(subclass)


class ValidDataClassProto(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            issubclass(subclass, DataClassProto) and not any(
                isinstance(f.type, InitVar) and f.default is MISSING and f.default_factory is MISSING
                for f in subclass.__dataclass_fields__.values()
            )
        )


class AnnotatedClassProto(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return _is_annotated_class(subclass) and getattr(subclass, "__is_annotated__", False)


class TypedDictProto(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return _is_annotated_class(subclass) and isinstance(subclass, type(TypedDict))


class NamedClassProto(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        if not _is_annotated_class(subclass):
            return False
        return issubclass(
            subclass,
            (NamedTupleProto, TypedDictProto, AnnotatedClassProto, ValidDataClassProto),
        )


@runtime_checkable
class ForwardRefProto(Protocol):
    __forward_arg__: str
