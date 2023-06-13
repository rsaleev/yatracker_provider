import typing
from datetime import date, datetime

from pydantic import root_validator, validator

from .base import SharedModel
from .common import (
    Attributes1,
    Attributes2,
    Attributes4,
    Attributes5,
    Attributes6,
    Attributes7,
    Attributes8,
    Relationship,
)


class IssueModel(SharedModel):
    self: str
    id: str
    key: str
    version: int
    last_comment_updated_at: typing.Optional[datetime]
    summary: str
    parent: typing.Optional[Attributes5]
    aliases: typing.Optional[typing.List[str]]
    description: typing.Optional[str]
    sprint: typing.Optional[typing.List[Attributes4]] = []
    type: Attributes6
    priority: Attributes6
    created_at: datetime
    followers: typing.Optional[typing.List[Attributes4]] = []
    created_by: Attributes4
    votes: typing.Optional[int]
    assignee: typing.Optional[typing.Optional[Attributes4]]
    queue: Attributes6
    updated_at: typing.Optional[datetime]
    status: Attributes6
    previous_status: typing.Optional[Attributes6]
    favorite: bool


class IssueImport(SharedModel):
    queue: typing.Union[Attributes6, str]
    summary: str
    created_at: datetime = datetime.now()
    created_by: typing.Union[Attributes6, str]
    key: typing.Optional[str]
    updated_at: typing.Optional[datetime] = None
    updated_by: typing.Optional[typing.Union[Attributes6, str]] = None
    resolved_at: typing.Optional[datetime] = None
    resolved_by: typing.Optional[typing.Union[Attributes6, str]] = None
    status: typing.Optional[str] = None
    deadline: typing.Optional[datetime] = None
    resolution: typing.Optional[str] = None
    type: typing.Optional[int] = None
    description: typing.Optional[str] = None
    start: typing.Optional[date] = None
    end: typing.Optional[date] = None
    assignee: typing.Optional[typing.Union[Attributes6, str]] = None
    priority: typing.Optional[typing.Union[Attributes6, int, str]] = None
    affected_versions: typing.Optional[typing.List[int]] = None
    fix_versions: typing.Optional[typing.List[int]] = None
    components: typing.Optional[typing.List[str]] = None
    tags: typing.Optional[typing.List[typing.Any]] = None
    sprint: typing.Optional[typing.List[typing.Union[Attributes6, str]]] = None
    followers: typing.Optional[typing.Union[str, Attributes4]] = None
    access: typing.Optional[typing.List[str]] = None
    unique: typing.Optional[typing.Any] = None
    following_maillist: typing.Optional[typing.List[str]] = None
    original_estimation: typing.Optional[int] = None
    estimation: typing.Optional[int] = None
    spent: typing.Optional[int] = None
    story_points: typing.Optional[float] = None
    voted_by: typing.Optional[typing.List[int]] = None
    favorited_by: typing.Optional[typing.List[int]] = None

    @validator("resolved_by")
    def validate_resolved_by(cls, arg):
        if cls["resolved_at"] and not arg:
            raise ValueError
        return arg

    @validator("resolution")
    def validate_resolution(cls, arg):
        if cls["resolved_at"] and not arg:
            raise ValueError
        return arg


class IssueImported(SharedModel):
    self: str
    id: str
    key: str
    version: int
    summary: str
    original_estimation: typing.Optional[str]
    estimation: typing.Optional[str]
    spent: typing.Optional[str]
    updated_by: typing.Optional[Attributes4]
    resolved_at: typing.Optional[datetime]
    start: typing.Optional[date]
    resolved_by: typing.Optional[Attributes4]
    description: typing.Optional[str]
    following_maillist: typing.Optional[typing.List[Attributes4]]
    fix_versions: typing.Optional[typing.List[Attributes4]]
    type: Attributes6
    priority: Attributes6
    resolution: typing.Optional[Attributes6]
    created_at: datetime
    followers: typing.Optional[typing.List[Attributes4]]
    assignee: typing.Optional[typing.List[Attributes4]]
    created_by: Attributes4
    comment_without_external_message_count: typing.Optional[int]
    votes: typing.Optional[int]
    affected_versions: typing.Optional[typing.List[Attributes4]]
    comment_with_external_message_count: typing.Optional[int]
    end: typing.Optional[date]
    deadline: typing.Optional[date]
    queue: Attributes6
    updated_at: typing.Optional[datetime]
    story_points: typing.Optional[float]
    status: Attributes6
    components: typing.Optional[typing.List[Attributes4]]
    access: typing.Optional[typing.List[Attributes4]]
    unique: str
    favorite: bool


class IssueCreate(SharedModel):
    queue: Attributes2
    summary: str
    parent: typing.Optional[Attributes2]
    type: typing.Optional[Attributes2]
    assignee: typing.Optional[str]
    attachment_ids: typing.Optional[typing.List[int]]
    description: typing.Optional[str]
    sprint: typing.Optional[typing.List[str]]
    priority: typing.Optional[Attributes2]
    followers: typing.Optional[typing.List[str]]
    assignee: typing.Optional[str]
    unique: typing.Optional[str]
    attachment_ids: typing.Optional[typing.List[int]]


class IssueCreated(IssueModel):
    pass


class IssueModify(SharedModel):
    summary: typing.Optional[str] = None
    parent: typing.Optional[Attributes8] = None
    description: typing.Optional[str] = None
    sprint: typing.Optional[typing.List[Attributes1]] = None
    type: typing.Optional[Attributes2] = None
    priority: typing.Optional[Attributes2] = None
    followers: typing.Optional[typing.List[str]] = None
    start: typing.Optional[date] = None
    end: typing.Optional[date] = None
    assignee: typing.Optional[int] = None
    priority: typing.Optional[int] = None
    affected_versions: typing.Optional[int] = None
    tags: typing.Optional[typing.List[typing.Union[str, int]]] = None
    sprint: typing.Optional[typing.List[int]] = None
    followers: typing.Optional[typing.List[int]] = None

    @root_validator(pre=True)
    def validate_non_empty(cls, values):
        if all([v is None for v in values]):
            raise ValueError("Empty request body")
        return values


class IssueLink(SharedModel):
    relationship: typing.Union[
        typing.Literal[Relationship.DEPENDS_ON],
        typing.Literal[Relationship.DUPLICATES],
        typing.Literal[Relationship.EPIC],
        typing.Literal[Relationship.DEPENDENT],
        typing.Literal[Relationship.DUPLICATED],
        typing.Literal[Relationship.EPIC],
        typing.Literal[Relationship.PARENT],
        typing.Literal[Relationship.SUBTASK],
        typing.Literal[Relationship.RELATES],
    ]
    issue: str


class IssueRelationship(SharedModel):
    self: str
    id: str
    type: IssueLink
    direction: str
    object: Attributes6
    created_by: Attributes4
    updated_by: Attributes4
    created_at: datetime
    updated_at: datetime


class IssueTransit(SharedModel):
    pass


class IssueTransited(SharedModel):
    self: str
    id: str
    to: Attributes6
    screen: Attributes7

class IssueSearch(SharedModel):
    filter:typing.Optional[typing.Dict[str, str]]
    query:typing.Optional[str]
    expand:typing.Optional[str]
    keys:typing.Optional[str]
    queue:typing.Optional[str]
