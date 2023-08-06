import pkg_resources

from ._annotations import (
    AnnotatedAlias,
    AnnotatedClassProto,
    DataClassProto,
    Empty,
    ForwardRefProto,
    GenericAlias,
    NamedClassProto,
    NamedTupleProto,
    TypedDictProto,
    ValidDataClassProto,
    empty,
)
from ._jsoncompatible import (
    JSONArray,
    JSONCompatible,
    JSONObject,
    JSONSchema,
    JSONSingle,
)

__version__ = pkg_resources.require(__name__)[0].version
