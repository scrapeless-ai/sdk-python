from .scraping import ScrapingService

class DeepSerpService(ScrapingService):
    def __init__(self, api_key: str, base_url: str, timeout: int):
        super().__init__(api_key, base_url, timeout) 