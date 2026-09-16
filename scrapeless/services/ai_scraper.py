from dataclasses import asdict
from typing import Any, Dict, Union
from urllib.parse import quote

from .base import BaseService
from ..types.ai_scraper import (
    AIScraperTaskRequest,
    AIScraperTaskResponse,
    AIScraperTaskResult,
)


class AIScraperService(BaseService):
    """Extract AI chat content through the v2 Scraper API without polling."""

    base_path = '/api/v2/scraper'

    def __init__(self, api_key: str, base_url: str, timeout: int = 30000):
        super().__init__(api_key, base_url, timeout, handle_response=lambda data: data)

    def create_task(
        self, request: Union[AIScraperTaskRequest, Dict[str, Any]]
    ) -> AIScraperTaskResponse:
        """Forward parameters and return the complete API JSON unchanged."""
        if isinstance(request, AIScraperTaskRequest):
            body = asdict(request)
            if request.webhook is None:
                body.pop('webhook')
        else:
            body = request
        return self.request(
            f'{self.base_path}/request', 'POST', body,
            additional_headers={'x-api-token': self.api_key},
        )

    def get_task_result(self, task_id: str) -> AIScraperTaskResult:
        """Return current status, result, and task failure messages unchanged."""
        return self.request(
            f'{self.base_path}/result/{quote(task_id, safe="")}', 'GET',
            additional_headers={'x-api-token': self.api_key},
        )
