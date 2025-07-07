from dataclasses import asdict
from typing import Optional
from ...error import ScrapelessError
from ...types.scraping_crawl import CrawlParams, CrawlResponse, CrawlStatusResponse, CrawlErrorsResponse, ErrorResponse
from .base import ScrapingCrawlBaseService

class CrawlService(ScrapingCrawlBaseService):
    def __init__(self, api_key: str, base_url: str, timeout: int):
        super().__init__(api_key, base_url, timeout)

    def crawl_url(self, url: str, params: Optional[CrawlParams] = None, poll_interval: int = 2) -> CrawlStatusResponse:
        json_data = {'url': url}
        if params:
            params_dict = asdict(params)
            json_data.update(params_dict)
        try:
            response = self.request('/api/v1/crawler/crawl', 'POST', json_data)
            if response.get('id'):
                return self.monitor_job_status(response['id'], poll_interval)
            else:
                raise ScrapelessError('Failed to start a crawl job')
        except Exception as error:
            raise ScrapelessError(str(error))

    def async_crawl_url(self, url: str, params: Optional[CrawlParams] = None) -> CrawlResponse:
        json_data = {'url': url}
        if params:
            params_dict = asdict(params)
            json_data.update(params_dict)
        try:
            response = self.request('/api/v1/crawler/crawl', 'POST', json_data)
            return response
        except Exception as error:
            raise ScrapelessError(str(error))

    def check_crawl_status(self, task_id: str) -> CrawlStatusResponse:
        if not task_id:
            raise ScrapelessError('No crawl ID provided')
        url = f'/api/v1/crawler/crawl/{task_id}'
        try:
            response = self.request(url, 'GET')
            all_data = response.get('data')
            if response.get('status') == 'completed':
                status_data = response
                if 'data' in status_data:
                    data = status_data['data']
                    while isinstance(status_data, dict) and 'next' in status_data:
                        if not data:
                            break
                        status_data = self.request(status_data['next'], 'GET')
                        data += status_data['data']
                    all_data = data
            resp = CrawlStatusResponse(
                success=response.get('success'),
                status=response.get('status'),
                total=response.get('total'),
                completed=response.get('completed'),
                data=all_data,
                error=response.get('error') if not response.get('success') and response.get('error') else None
            )
            return resp
        except Exception as error:
            raise ScrapelessError(str(error))

    def check_crawl_errors(self, task_id: str) -> CrawlErrorsResponse:
        try:
            response = self.request(f'/api/v1/crawler/crawl/{task_id}/errors', 'DELETE')
            return response
        except Exception as error:
            raise ScrapelessError(str(error))

    def cancel_crawl(self, task_id: str) -> ErrorResponse:
        try:
            response = self.request(f'/api/v1/crawler/crawl/{task_id}', 'DELETE')
            return response
        except Exception as error:
            raise ScrapelessError(str(error))