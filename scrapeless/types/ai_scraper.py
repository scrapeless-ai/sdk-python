from dataclasses import dataclass
from typing import Any, Dict, Optional, TypedDict


@dataclass
class AIScraperTaskRequest:
    """Actor-specific input and an optional webhook containing a callback URL."""

    actor: str
    input: Dict[str, Any]
    webhook: Optional[Dict[str, Any]] = None


class _AIScraperResultFields(TypedDict, total=False):
    message: str
    task_result: Any


class AIScraperTaskResult(_AIScraperResultFields):
    """Raw result JSON; known statuses are success, failed, and running."""

    status: str


class AIScraperTaskResponse(AIScraperTaskResult):
    task_id: str
