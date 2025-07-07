from typing import Optional
from ..services import ScrapingCrawlService
from ..types.scraping_crawl import ScrapeParams, CrawlParams
from ..env import get_env, get_env_with_default

class ScrapingCrawl:
    """
    High-level ScrapingCrawl SDK class that provides unified access to scraping, crawling services.
    """
    def __init__(self, config: dict):
        api_key = config.get('api_key') or get_env('SCRAPELESS_API_KEY')
        base_url = config.get('base_url') or get_env_with_default('SCRAPELESS_CRAWL_API_URL', 'https://api.scrapeless.com')
        timeout = config.get('timeout') or 0
        self.service = ScrapingCrawlService(api_key, base_url, timeout)

    def scrape_url(self, url: str, params: Optional[ScrapeParams] = None):
        return self.service.scrape.scrape_url(url, params)

    def async_scrape_url(self, url: str, params: Optional[ScrapeParams] = None):
        return self.service.scrape.async_scrape_url(url, params)

    def check_scrape_status(self, task_id: str):
        return self.service.scrape.check_scrape_status(task_id)

    def batch_scrape_urls(self, urls: list, params: Optional[ScrapeParams] = None, poll_interval: int = 2, ignore_invalid_urls: bool = False):
        return self.service.scrape.batch_scrape_urls(urls, params, poll_interval, ignore_invalid_urls)

    def async_batch_scrape_urls(self, urls: list, params: Optional[ScrapeParams] = None, ignore_invalid_urls: bool = False):
        return self.service.scrape.async_batch_scrape_urls(urls, params, ignore_invalid_urls)

    def check_batch_scrape_status(self, task_id: str):
        return self.service.scrape.check_batch_scrape_status(task_id)

    def crawl_url(self, url: str, params: Optional[CrawlParams] = None, poll_interval: int = 2):
        return self.service.crawl.crawl_url(url, params, poll_interval)

    def async_crawl_url(self, url: str, params: Optional[CrawlParams] = None):
        return self.service.crawl.async_crawl_url(url, params)

    def check_crawl_status(self, task_id: str):
        return self.service.crawl.check_crawl_status(task_id)

    def check_crawl_errors(self, task_id: str):
        return self.service.crawl.check_crawl_errors(task_id)

    def cancel_crawl(self, task_id: str):
        return self.service.crawl.cancel_crawl(task_id)

    def monitor_job_status(self, task_id: str, poll_interval: int):
        return self.service.crawl.monitor_job_status(task_id, poll_interval)