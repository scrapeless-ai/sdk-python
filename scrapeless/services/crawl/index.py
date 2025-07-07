from .scrape import ScrapeService
from .crawl import CrawlService

class ScrapingCrawlService:
    """
    Aggregates ScrapeService and CrawlService for unified access
    """
    def __init__(self, api_key: str, base_url: str, timeout: int):
        self.scrape = ScrapeService(api_key, base_url, timeout)
        self.crawl = CrawlService(api_key, base_url, timeout)