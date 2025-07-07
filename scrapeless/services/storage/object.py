from ..base import BaseService
from ...types.storage import IObjectCreateParams, IObjectUploadParams
from urllib.parse import urlencode
from dataclasses import asdict

class ObjectStorage(BaseService):
    base_path = '/api/v1/object'

    def list_buckets(self, params):
        query = {
            'page': params.page,
            'pageSize': params.pageSize
        }
        if getattr(params, 'desc', None) is not None:
            query['desc'] = '1' if params.desc else '0'
        if getattr(params, 'actor', None):
            query['actor'] = params.actor
        if getattr(params, 'runId', None):
            query['runId'] = params.runId
        query_str = urlencode(query)
        return self.request(f"{self.base_path}/buckets?{query_str}")

    def create_bucket(self, data: IObjectCreateParams):
        payload_dict = asdict(data)
        return self.request(f"{self.base_path}/buckets", 'POST', payload_dict)

    def delete_bucket(self, bucket_id: str):
        return self.request(f"{self.base_path}/buckets/{bucket_id}", 'DELETE')

    def get_bucket(self, bucket_id: str):
        return self.request(f"{self.base_path}/buckets/{bucket_id}")

    def list(self, bucket_id: str, params):
        query = {
            'page': params.page,
            'pageSize': params.page_size
        }
        if getattr(params, 'search', None):
            query['search'] = params.search
        query_str = urlencode(query)
        return self.request(f"{self.base_path}/buckets/{bucket_id}/objects?{query_str}")

    def get(self, bucket_id: str, object_id: str):
        return self.request(f"{self.base_path}/buckets/{bucket_id}/{object_id}")

    def put(self, bucket_id: str, data: IObjectUploadParams):
        files = {'file': open(data.file, 'rb')}
        payload = {}
        if getattr(data, 'actorId', None):
            payload['actorId'] = data.actor_id
        if getattr(data, 'runId', None):
            payload['runId'] = data.run_id
        return self.request(f"{self.base_path}/buckets/{bucket_id}/object", 'POST', files)

    def delete(self, bucket_id: str, object_id: str):
        return self.request(f"{self.base_path}/buckets/{bucket_id}/{object_id}", 'DELETE') 