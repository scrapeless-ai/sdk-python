from dataclasses import dataclass
from typing import Optional, Dict, Any

"""
Scraping request parameters
"""
@dataclass
class ScrapingTaskRequest:
    actor: str
    input: Dict[str, Any]
    proxy: Optional[Dict[str, Any]] = None
    async_: Optional[bool] = None  # 'async' is a reserved word in Python
    # Additional options can be added as needed

"""
Task response from API
"""
@dataclass
class ScrapingTaskResponse:
    message: str
    taskId: str
    # Additional fields can be added as needed 