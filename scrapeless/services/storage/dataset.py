from ..base import BaseService
from ...types.storage import IDatasetListParams, IPaginationParams
from urllib.parse import urlencode

class DatasetStorage(BaseService):
    base_path = '/api/v1/dataset'

    def list_datasets(self, params: IDatasetListParams):
        query = {
            'page': params.page,
            'pageSize': params.page_size
        }
        if getattr(params, 'desc', None) is not None:
            query['desc'] = bool(params.desc)
        if getattr(params, 'actorId', None) is not None:
            query['actorId'] = params.actor_id
        if getattr(params, 'runId', None) is not None:
            query['runId'] = params.run_id
        query_str = urlencode(query)
        return self.request(f"{self.base_path}?{query_str}")

    def create_dataset(self, name: str):
        return self.request(f"{self.base_path}", 'POST', {'name': name})

    def update_dataset(self, dataset_id: str, name: str):
        return self.request(f"{self.base_path}/{dataset_id}", 'PUT', {'name': name})

    def del_dataset(self, dataset_id: str):
        return self.request(f"{self.base_path}/{dataset_id}", 'DELETE')

    def add_items(self, dataset_id: str, items: list):
        return self.request(f"{self.base_path}/{dataset_id}/items", 'POST', {'items': items})

    def get_items(self, dataset_id: str, params: IPaginationParams):
        query = {
            'page': params.page,
            'pageSize': params.page_size
        }
        if getattr(params, 'desc', None) is not None:
            query['desc'] = bool(params.desc)
        query_str = urlencode(query)
        return self.request(f"{self.base_path}/{dataset_id}/items?{query_str}")

    def get_dataset(self, dataset_id: str):
        return self.request(f"{self.base_path}/{dataset_id}") 