from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ProfileItem:
    profileId: str
    name: str
    createdAt: datetime
    updatedAt: datetime

@dataclass
class CreateProfileResponse:
    profileId: str
    name: str
    createdAt: datetime
    updatedAt: datetime

@dataclass
class DeleteProfileResponse:
    success: bool

@dataclass
class ProfilePaginationParams:
    page: int
    page_size: int
    name: Optional[str] = None
