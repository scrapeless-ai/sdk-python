from dataclasses import asdict
from .base import BaseService
from ..types.universal import UniversalScrapingRequest

"""
UniversalService for scraping any website using the Universal Scraping API
"""
class UniversalService(BaseService):
    base_path = '/api/v1/unlocker'
    def __init__(self, api_key: str, base_url: str, timeout: int):
        super().__init__(api_key, base_url, timeout)

    def scrape(self, request: UniversalScrapingRequest):
        payload_dict = asdict(request)
        return self.request(f"{self.base_path}/request", 'POST', payload_dict)