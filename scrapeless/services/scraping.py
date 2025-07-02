from dataclasses import asdict
from .base import BaseService
from ..utils.utils import sleep
from ..types.scraping import ScrapingTaskRequest

"""
ScrapingService for extracting data from websites
"""
class ScrapingService(BaseService):
    base_path = '/api/v1/scraper'

    def __init__(self, api_key: str, base_url: str, timeout: int):
        super().__init__(api_key, base_url, timeout)

    def create_task(self, request: ScrapingTaskRequest):
        payload_dict = asdict(request)
        request_with_sync = payload_dict.copy()
        request_with_sync['async'] = True
        return self.request(f"{self.base_path}/request", 'POST', request_with_sync, response_with_status=True)

    def get_task_result(self, task_id: str):
        return self.request(f"{self.base_path}/result/{task_id}", 'GET', response_with_status=True)

    def scrape(self, request: ScrapingTaskRequest):
        payload_dict = asdict(request)
        request_with_sync = payload_dict.copy()
        response = self.create_task(ScrapingTaskRequest(**request_with_sync))
        if response['status'] == 200:
            return response['data']
        while True:
            sleep(1000)
            result = self.get_task_result(response['data']['taskId'])
            if result['status'] == 200:
                return result['data'] 