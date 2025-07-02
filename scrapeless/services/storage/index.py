from ..base import BaseService
from .dataset import DatasetStorage
from .kv import KVStorage
from .object import ObjectStorage
from .queue import QueueStorage

class StorageService(BaseService):
    """
    StorageService provides access to all Actor storage services
    """
    def __init__(self, api_key: str, base_url: str, timeout: int):
        super().__init__(api_key, base_url, timeout)
        self.dataset = DatasetStorage(api_key, base_url, timeout)
        self.kv = KVStorage(api_key, base_url, timeout)
        self.object = ObjectStorage(api_key, base_url, timeout)
        self.queue = QueueStorage(api_key, base_url, timeout) 