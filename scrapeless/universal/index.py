from typing import Optional
from ..services import UniversalService
from ..env import get_env, get_env_with_default
from ..types.universal import (
    UniversalScrapingRequest,
    UniversalJsRenderInput,
    UniversalWebUnlockerInput,
    UniversalAkamaiWebCookieInput,
    UniversalAkamaiWebSensorInput,
    UniversalConfig,
    UniversalProxy
)

class Universal:
    """
    Universal scraping service for various scraping scenarios
    """
    def __init__(self, config: Optional[UniversalConfig] = None):
        if config is None:
            config = UniversalConfig()
        self.api_key = config.api_key or get_env('SCRAPELESS_API_KEY')
        self.base_api_url = get_env_with_default('SCRAPELESS_BASE_API_URL', 'https://api.scrapeless.com')
        self.timeout = config.timeout or 30000
        self.universal_service = UniversalService(self.api_key, self.base_api_url, self.timeout)

    def js_render(self, data: UniversalScrapingRequest[UniversalJsRenderInput, UniversalProxy]):
        return self.universal_service.scrape(data)

    def web_unlocker(self, data: UniversalScrapingRequest[UniversalWebUnlockerInput, UniversalProxy]):
        return self.universal_service.scrape(data)

    def akamai_web_cookie(self, data: UniversalScrapingRequest[UniversalAkamaiWebCookieInput, UniversalProxy]):
        return self.universal_service.scrape(data)

    def akamai_web_sensor(self, data: UniversalScrapingRequest[UniversalAkamaiWebSensorInput, UniversalProxy]):
        return self.universal_service.scrape(data)