from dataclasses import dataclass
from typing import Optional

@dataclass
class ScrapelessConfig:
    baseApiUrl: Optional[str] = None
    actorApiUrl: Optional[str] = None
    storageApiUrl: Optional[str] = None
    browserApiUrl: Optional[str] = None
    scrapingCrawlApiUrl: Optional[str] = None
    apiKey: Optional[str] = None
    timeout: Optional[int] = None 