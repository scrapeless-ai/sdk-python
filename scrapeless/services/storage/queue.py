from typing import Optional
from ..base import BaseService
from ...types.storage import IQueueCreateParams, IQueueUpdateParams, IQueuePushParams, IPaginationParams
from urllib.parse import urlencode
from dataclasses import asdict

class QueueStorage(BaseService):
    base_path = '/api/v1/queue'

    def list(self, params: IPaginationParams):
        query = {
            'page': params.page,
            'pageSize': params.page_size
        }
        if getattr(params, 'desc', None) is not None:
            query['desc'] = bool(params.desc)
        query_str = urlencode(query)
        return self.request(f"{self.base_path}/queues?{query_str}")

    def create(self, data: IQueueCreateParams):
        payload_dict = asdict(data)
        return self.request(f"{self.base_path}", 'POST', payload_dict)

    def get(self, name: str, queue_id: Optional[str] = None):
        query = {'name': name}
        if queue_id:
            query['id'] = queue_id
        query_str = urlencode(query)
        return self.request(f"{self.base_path}?{query_str}")

    def update(self, queue_id: str, data: IQueueUpdateParams):
        payload_dict = asdict(data)
        return self.request(f"{self.base_path}/{queue_id}", 'PUT', payload_dict)

    def delete(self, queue_id: str):
        return self.request(f"{self.base_path}/{queue_id}", 'DELETE')

    def push(self, queue_id: str, params: IQueuePushParams):
        payload_dict = asdict(params)
        return self.request(f"{self.base_path}/{queue_id}/push", 'POST', payload_dict)

    def pull(self, queue_id: str, limit: Optional[int] = None):
        if limit:
            query = {'limit': limit}
            query_str = urlencode(query)
            return self.request(f"{self.base_path}/{queue_id}/pull?{query_str}")
        return self.request(f"{self.base_path}/{queue_id}/pull")

    def ack(self, queue_id: str, msg_id: str):
        return self.request(f"{self.base_path}/{queue_id}/ack/{msg_id}", 'POST') 