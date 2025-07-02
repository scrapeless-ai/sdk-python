from ..base import BaseService
from ...types.storage import IKVValueData, IPaginationParams
from urllib.parse import urlencode

class KVStorage(BaseService):
    base_path = '/api/v1/kv'

    def list_namespaces(self, params: IPaginationParams):
        query = {
            'page': params.page,
            'pageSize': params.page_size
        }
        if getattr(params, 'desc', None) is not None:
            query['desc'] = bool(params.desc)
        query_str = urlencode(query)
        return self.request(f"{self.base_path}/namespaces?{query_str}")

    def create_namespace(self, name: str):
        return self.request(f"{self.base_path}/namespaces", 'POST', {'name': name})

    def get_namespace(self, namespace_id: str):
        return self.request(f"{self.base_path}/{namespace_id}")

    def del_namespace(self, namespace_id: str):
        return self.request(f"{self.base_path}/{namespace_id}", 'DELETE')

    def rename_namespace(self, namespace_id: str, name: str):
        return self.request(f"{self.base_path}/{namespace_id}/rename", 'PUT', {'name': name})

    def list_keys(self, namespace_id: str, params: IPaginationParams):
        query = {
            'page': params.page,
            'pageSize': params.page_size
        }
        query_str = urlencode(query)
        return self.request(f"{self.base_path}/{namespace_id}/keys?{query_str}")

    def del_value(self, namespace_id: str, key: str):
        return self.request(f"{self.base_path}/{namespace_id}/{key}", 'DELETE')

    def bulk_set_value(self, namespace_id: str, data: list):
        return self.request(f"{self.base_path}/{namespace_id}/bulk", 'POST', {'Items': data})

    def bulk_del_value(self, namespace_id: str, keys: list):
        return self.request(f"{self.base_path}/{namespace_id}/bulk", 'POST', {'keys': keys})

    def set_value(self, namespace_id: str, data: IKVValueData):
        return self.request(f"{self.base_path}/{namespace_id}/key", 'PUT', {'key': data.key, 'value': data.value, 'expiration': data.expiration})

    def get_value(self, namespace_id: str, key: str):
        return self.request(f"{self.base_path}/{namespace_id}/{key}") 