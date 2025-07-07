from dataclasses import dataclass
from typing import Optional

@dataclass
class ScrapelessConfig:
    base_api_url: Optional[str] = None
    actor_api_url: Optional[str] = None
    storage_api_url: Optional[str] = None
    browser_api_url: Optional[str] = None
    scraping_crawl_api_url: Optional[str] = None
    api_key: Optional[str] = None
    timeout: Optional[int] = None 