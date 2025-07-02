from ..base import BaseService
from ...error import ScrapelessError
from ...types.scraping_crawl import CrawlStatusResponse
import time

class ScrapingCrawlBaseService(BaseService):
    def __init__(self, api_key: str, base_url: str, timeout: int):
        super().__init__(api_key, base_url, timeout, handle_response=lambda res: res)

    def monitor_job_status(self, task_id: str, poll_interval: int) -> CrawlStatusResponse:
        try:
            while True:
                status_response = self.request(f"/api/v1/crawler/crawl/{task_id}", 'GET')
                if status_response.get('status') == 'completed':
                    if 'data' in status_response:
                        data = status_response['data']
                        while isinstance(status_response, dict) and 'next' in status_response:
                            if not data:
                                break
                            status_response = self.request(status_response['next'], 'GET')
                            data += status_response['data']
                        status_response['data'] = data
                        return status_response
                    else:
                        raise ScrapelessError('Crawl job completed but no data was returned')
                elif status_response.get('status') in ['active', 'paused', 'pending', 'queued', 'waiting', 'scraping']:
                    poll_interval = max(poll_interval, 2)
                    time.sleep(poll_interval)
                else:
                    raise ScrapelessError(f"Crawl job failed or was stopped. Status: {status_response.get('status')}")
        except Exception as error:
            raise ScrapelessError(str(error))