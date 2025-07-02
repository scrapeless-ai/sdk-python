from dataclasses import dataclass
from typing import Optional, Any, Dict, List, TypeVar, Generic
from datetime import datetime

"""
Actor run options
"""
@dataclass
class ActorRunOptions:
    CPU: Optional[int] = None
    memory: Optional[int] = None
    timeout: Optional[int] = None

"""
Actor creation data
"""
@dataclass
class ActorCreateRequest:
    description: Optional[str]
    gitRepo: str
    isPublic: Optional[bool]
    name: str
    defaultRunOptions: Optional[ActorRunOptions]
    title: str
    version: str

"""
Actor run data
"""
T = TypeVar('T')
@dataclass
class ActorRunRequest(Generic[T]):
    input: T
    runOptions: Optional[ActorRunOptions] = None

"""
Actor run result
"""
@dataclass
class ActorRunResult(Generic[T]):
    actorId: str
    finishedAt: datetime
    input: T
    runId: str
    runOptions: ActorRunOptions
    startedAt: datetime
    stats: Dict[str, Any]
    status: str
    teamId: str
    userId: str

"""
Actor update data
"""
ActorUpdateRequest = Optional[ActorCreateRequest]

"""
Actor build response
"""
@dataclass
class ActorBuildResponse:
    buildId: str
    finishedAt: str
    logs: List[str]
    message: str
    startedAt: str
    status: str

@dataclass
class IActorRunOptions:
    CPU: Optional[int] = None
    memory: Optional[int] = None
    timeout: Optional[int] = None

@dataclass
class IRunActorData(Generic[T]):
    input: T
    run_options: IActorRunOptions