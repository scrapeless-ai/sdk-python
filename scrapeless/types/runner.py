from dataclasses import dataclass
from typing import Optional, Dict, Any

"""
Runner interface
"""
@dataclass
class Runner:
    id: str
    name: str
    description: Optional[str]
    actorId: str
    config: Dict[str, Any]
    env: Dict[str, str]
    memoryMb: int
    timeoutSecs: int
    version: str
    createdAt: str
    updatedAt: str
    createdBy: str 