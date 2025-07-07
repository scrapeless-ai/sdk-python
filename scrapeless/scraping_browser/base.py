from abc import ABC
from typing import Optional

from ..types.config import ScrapelessConfig
from ..services import BrowserService
from ..env import get_env, get_env_with_default
from ..utils import Logger

def create_logger(prefix: str):
    """Create a base logger that can be extended by specific implementations"""
    return Logger().with_prefix(prefix)

class BaseBrowser(ABC):
    """
    Base browser service configuration
    """
    browser_service: Optional[BrowserService] = None

    def __init__(self):
        """
        Base constructor for browser implementations
        """
        pass

    def _init_browser_service(self, config: Optional[ScrapelessConfig] = None):
        """
        Initialize browser service with Scrapeless configuration
        :param config: Optional Scrapeless configuration
        """
        if config is None:
            config = ScrapelessConfig()

        api_key = config.api_key or get_env('SCRAPELESS_API_KEY')
        browser_url = config.base_api_url or get_env_with_default('SCRAPELESS_BROWSER_API_URL', 'https://browser.scrapeless.com')
        
        timeout = config.timeout if config.timeout is not None else 30000
        self.browser_service = BrowserService(api_key, browser_url, timeout) 