from .base import BaseService
from ..types.storage import IPaginationParams
from ..types.actor import IRunActorData
from urllib.parse import urlencode
from dataclasses import asdict

"""
Actor service class for interacting with the Scrapeless Actor API
"""
class ActorService(BaseService):
    base_path = '/api/v1/actors'

    def __init__(self, api_key: str, base_url: str, timeout: int):
        super().__init__(api_key, base_url, timeout)

    def run(self, actor_id: str, data: IRunActorData):
        payload_dict = asdict(data)
        return self.request(f"{self.base_path}/{actor_id}/runs", 'POST', payload_dict)

    def get_run_info(self, run_id: str):
        return self.request(f"{self.base_path}/runs/{run_id}")

    def abort_run(self, actor_id: str, run_id: str):
        return self.request(f"{self.base_path}/{actor_id}/runs/{run_id}", 'DELETE')

    def build(self, actor_id: str):
        return self.request(f"{self.base_path}/{actor_id}/builds", 'POST')

    def get_build_status(self, actor_id: str, build_id: str):
        return self.request(f"{self.base_path}/{actor_id}/builds/{build_id}")

    def abort_build(self, actor_id: str, build_id: str):
        return self.request(f"{self.base_path}/{actor_id}/builds/{build_id}", 'DELETE')

    def get_run_list(self, params: IPaginationParams):
        query = {
            'page': params.page,
            'pageSize': params.page_size
        }
        if getattr(params, 'desc', None) is not None:
            query['desc'] = '1' if params.desc else '0'
        query_str = urlencode(query)
        return self.request(f"{self.base_path}/runs?{query_str}") 