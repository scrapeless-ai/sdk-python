from dataclasses import asdict
from typing import Optional
from ...error import ScrapelessError
from ...types.scraping_crawl import ScrapeParams
from .base import ScrapingCrawlBaseService
import time

class ScrapeService(ScrapingCrawlBaseService):
    def __init__(self, api_key: str, base_url: str, timeout: int):
        super().__init__(api_key, base_url, timeout)

    def scrape_url(self, url: str, params: Optional[ScrapeParams] = None, poll_interval: int = 2):
        json_data = {'url': url}
        if params:
            params_dict = asdict(params)
            json_data.update(params_dict)
        try:
            response = self.request('/api/v1/crawler/scrape', 'POST', json_data)
            if not response.get('id'):
                raise ScrapelessError('Failed to start a scrape job')
            while True:
                status_response = self.check_scrape_status(response['id'])
                if status_response.get('status') != 'scraping':
                    return status_response
                poll_interval = max(poll_interval, 2)
                time.sleep(poll_interval)
        except Exception as error:
            raise ScrapelessError(str(error))

    def async_scrape_url(self, url: str, params: Optional[ScrapeParams] = None):
        json_data = {'url': url}
        if params:
            params_dict = asdict(params)
            json_data.update(params_dict)
        try:
            response = self.request('/api/v1/crawler/scrape', 'POST', json_data)
            return response
        except Exception as error:
            raise ScrapelessError(str(error))

    def check_scrape_status(self, task_id: str):
        if not task_id:
            raise ScrapelessError('No scrape ID provided')
        url = f'/api/v1/crawler/scrape/{task_id}'
        try:
            response = self.request(url, 'GET')
            return response
        except Exception as error:
            raise ScrapelessError(str(error))

    def batch_scrape_urls(self, urls: list, params: Optional[ScrapeParams] = None, poll_interval: int = 2, ignore_invalid_urls: bool = False):
        json_data = {'urls': urls, 'ignoreInvalidURLs': ignore_invalid_urls}
        if params:
            params_dict = asdict(params)
            json_data.update(params_dict)
        try:
            response = self.request('/api/v1/crawler/scrape/batch', 'POST', json_data)
            if not response.get('id'):
                raise ScrapelessError('Failed to start a batch scrape job')
            while True:
                status_response = self.check_batch_scrape_status(response['id'])
                if status_response.get('status') != 'scraping':
                    return status_response
                poll_interval = max(poll_interval, 2)
                time.sleep(poll_interval)
        except Exception as error:
            raise ScrapelessError(str(error))

    def async_batch_scrape_urls(self, urls: list, params: Optional[ScrapeParams] = None, ignore_invalid_urls: bool = False):
        json_data = {'urls': urls, 'ignoreInvalidURLs': ignore_invalid_urls}
        if params:
            params_dict = asdict(params)
            json_data.update(params_dict)
        try:
            response = self.request('/api/v1/crawler/scrape/batch', 'POST', json_data)
            return response
        except Exception as error:
            raise ScrapelessError(str(error))

    def check_batch_scrape_status(self, task_id: str):
        if not task_id:
            raise ScrapelessError('No scrape ID provided')
        url = f'/api/v1/crawler/scrape/batch/{task_id}'
        try:
            response = self.request(url, 'GET')
            return response
        except Exception as error:
            raise ScrapelessError(str(error)) 