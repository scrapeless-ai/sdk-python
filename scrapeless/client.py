from typing import Optional

from .services import (
    BrowserService,
    ScrapingService,
    DeepSerpService,
    UniversalService,
    ProxiesService,
    ActorService,
    StorageService,
    ScrapingCrawlService,
    # CaptchaService,
)
from .env import get_env, get_env_with_default
from .error import ScrapelessError

class Scrapeless:
    def __init__(self, config: Optional[dict] = None):
        if config is None:
            config = {}
        api_key = config.get('api_key') or get_env('SCRAPELESS_API_KEY')
        timeout = config.get('timeout', 30000)
        base_api_url = config.get('base_api_url') or get_env_with_default('SCRAPELESS_BASE_API_URL', 'https://api.scrapeless.com')
        actor_url = config.get('actor_api_url') or get_env_with_default('SCRAPELESS_ACTOR_API_URL', 'https://actor.scrapeless.com')
        storage_url = config.get('storage_api_url') or get_env_with_default('SCRAPELESS_STORAGE_API_URL', 'https://storage.scrapeless.com')
        browser_url = config.get('browser_api_url') or get_env_with_default('SCRAPELESS_BROWSER_API_URL', 'https://browser.scrapeless.com')
        scraping_crawl_url = config.get('scraping_crawl_api_url') or get_env_with_default('SCRAPELESS_CRAWL_API_URL', 'https://api.scrapeless.com')

        if not api_key:
            raise ScrapelessError(
                'API key is required - either pass it in config or set SCRAPELESS_API_KEY environment variable'
            )

        self.actor = ActorService(api_key, actor_url, timeout)
        self.browser = BrowserService(api_key, browser_url, timeout)
        self.storage = StorageService(api_key, storage_url, timeout)
        self.scraping = ScrapingService(api_key, base_api_url, timeout)
        self.deepserp = DeepSerpService(api_key, base_api_url, timeout)
        self.universal = UniversalService(api_key, base_api_url, timeout)
        self.proxies = ProxiesService(api_key, base_api_url, timeout)
        # self.captcha = CaptchaService(api_key, base_api_url, timeout)
        self.scraping_crawl = ScrapingCrawlService(api_key, scraping_crawl_url, config.get('timeout', 0))