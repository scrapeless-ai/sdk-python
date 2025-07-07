import datetime
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

"""
Pagination interface for list operations
"""
@dataclass
class IPagination:
    total: int
    totalPage: int
    page: int
    pageSize: int
    items: List[Any]

@dataclass
class IPaginationParams:
    page: int
    page_size: int
    desc: Optional[bool] = None

@dataclass
class IStorageCommonResponse:
    success: bool
    message: Optional[str] = None

ICommonResponse = Dict[str, Any]  # Pick<IStorageCommonResponse, 'success'>

@dataclass
class IDatasetListParams(IPaginationParams):
    actor_id: Optional[str] = None
    run_id: Optional[str] = None

@dataclass
class IDatasetCreateParams:
    name: str
    actorId: Optional[str] = None
    runId: Optional[str] = None

@dataclass
class IDataset:
    id: str
    name: str
    actorId: str
    runId: str
    fields: Optional[List[str]]
    createdAt: str
    updatedAt: str
    stats: Dict[str, Any]

@dataclass
class IKVNamespace:
    actorId: str
    createdAt: str
    id: str
    name: str
    runId: str
    updatedAt: str
    stats: Dict[str, Any]

@dataclass
class IKVNamespaceCreateParams:
    name: str
    actorId: Optional[str] = None
    runId: Optional[str] = None

@dataclass
class IKVItem:
    key: str
    size: int

@dataclass
class IKVValueData:
    key: str
    value: str
    expiration: Optional[int] = None

@dataclass
class IObjectCreateParams:
    name: str
    description: Optional[str] = None

@dataclass
class IObjectUploadParams:
    file: str
    actor_id: Optional[str] = None
    run_id: Optional[str] = None

@dataclass
class IQueueCreateParams:
    name: str
    actor_id: str
    run_id: str
    description: Optional[str] = None

@dataclass
class IQueueUpdateParams:
    name: Optional[str] = None
    description: Optional[str] = None

@dataclass
class IQueuePushParams:
    name: str
    payload: str
    retry: int
    timeout: int
    deadline: datetime