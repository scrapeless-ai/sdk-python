from .base import BaseService
from ..types.profile import ProfilePaginationParams
from urllib.parse import urlencode

"""
ProfileService for use browser profile
"""
class ProfilesService(BaseService):
    base_path = '/browser/profiles'

    def __init__(self, api_key: str, base_url: str, timeout: int):
        super().__init__(api_key, base_url, timeout)

    def create(self, name: str):
        response = self.request(f"{self.base_path}", "POST", {'name': name}, response_with_status=True)
        return response['data']

    def get(self, profile_id: str):
        response = self.request(f"{self.base_path}/{profile_id}", 'GET', response_with_status=True)
        return response['data']

    def delete(self, profile_id: str):
        response = self.request(f"{self.base_path}/{profile_id}", 'DELETE', response_with_status=True)
        return response['data']

    def list(self, params: ProfilePaginationParams):
        query = {
            'page': params.page,
            'pageSize': params.page_size
        }
        if getattr(params, 'name', None) is not None:
            query['name'] = params.name
        query_str = urlencode(query)
        response = self.request(f"{self.base_path}?{query_str}", 'GET', response_with_status=True)
        return response['data']
