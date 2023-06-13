from enum import StrEnum
from .base import SharedModel

class Attributes1(SharedModel):
    id: str


class Attributes2(SharedModel):
    id: str
    key: str


class Attributes3(SharedModel):
    id: str
    display: str


class Attributes4(SharedModel):
    self: str
    id: str
    display: str


class Attributes5(SharedModel):
    self: str
    id: str
    key: str


class Attributes6(SharedModel):
    self: str
    id: str
    key: str
    display: str


class Attributes7(SharedModel):
    self: str
    id: str


class Attributes8(SharedModel):
    key: str


class Relationship(StrEnum):
    RELATES = "relates"
    DEPENDENT = "dependent"
    DEPENDS_ON = "depends"
    SUBTASK = "subtask"
    PARENT = "parent"
    DUPLICATES = "duplicates"
    DUPLICATED = "duplicated"
    EPIC = "epic"