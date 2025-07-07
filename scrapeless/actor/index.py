from typing import Optional
from ..services import StorageService, BrowserService
from ..env import get_env, get_env_with_default
from ..types import (
    IPaginationParams,
    IDatasetListParams,
    IKVValueData,
    IObjectCreateParams,
    IObjectUploadParams,
    IQueueCreateParams,
    IQueueUpdateParams,
    IQueuePushParams
)

"""
High-level Actor class that integrates various Scrapeless services
"""
class Actor:
    def __init__(self):
        # Get API key from environment
        timeout = 30000
        api_key = get_env('SCRAPELESS_API_KEY')
        storage_url = get_env_with_default('SCRAPELESS_STORAGE_API_URL', 'https://storage.scrapeless.com')
        browser_url = get_env_with_default('SCRAPELESS_BROWSER_API_URL', 'https://browser.scrapeless.com');

        self.dataset_id = get_env('SCRAPELESS_DATASET_ID')
        self.namespace_id = get_env('SCRAPELESS_KV_NAMESPACE_ID')
        self.bucket_id = get_env('SCRAPELESS_BUCKET_ID')
        self.queue_id = get_env('SCRAPELESS_QUEUE_ID')

        # Initialize all services
        self.storage = StorageService(api_key, storage_url, timeout)
        self.browser = BrowserService(api_key, browser_url, timeout)

    def input(self):
        """
        Get actor input data from environment variable
        :return: Actor input data parsed from environment variable
        """
        import json
        input_str = self.get_value('INPUT')
        return json.loads(input_str)

    # Dataset convenience methods with environment variables
    def list_datasets(self, params: IDatasetListParams):
        return self.storage.dataset.list_datasets(params)

    def add_items(self, items: list):
        return self.storage.dataset.add_items(self.dataset_id, items)

    def get_items(self, params: IPaginationParams):
        return self.storage.dataset.get_items(self.dataset_id, params)

    def update_dataset(self, name: str):
        return self.storage.dataset.update_dataset(self.dataset_id, name)

    def delete_dataset(self):
        return self.storage.dataset.del_dataset(self.dataset_id)

    def get_dataset(self):
        return self.storage.dataset.get_dataset(self.dataset_id)

    # KV store convenience methods with environment variables
    def list_namespaces(self, params: IPaginationParams):
        return self.storage.kv.list_namespaces(params)

    def create_namespace(self, name: str):
        return self.storage.kv.create_namespace(name)

    def get_namespace(self):
        return self.storage.kv.get_namespace(self.namespace_id)

    def delete_namespace(self):
        return self.storage.kv.del_namespace(self.namespace_id)

    def rename_namespace(self, name: str):
        return self.storage.kv.rename_namespace(self.namespace_id, name)

    def list_keys(self, params: IPaginationParams):
        return self.storage.kv.list_keys(self.namespace_id, params)

    def delete_value(self, key: str):
        return self.storage.kv.del_value(self.namespace_id, key)

    def bulk_set_value(self, data: list):
        return self.storage.kv.bulk_set_value(self.namespace_id, data)

    def bulk_del_value(self, keys: list):
        return self.storage.kv.bulk_del_value(self.namespace_id, keys)

    def set_value(self, data: IKVValueData):
        return self.storage.kv.set_value(self.namespace_id, data)

    def get_value(self, key: str):
        return self.storage.kv.get_value(self.namespace_id, key)

    # Object storage convenience methods with environment variables
    def list_buckets(self, params: IPaginationParams):
        return self.storage.object.list_buckets(params)

    def create_bucket(self, data: IObjectCreateParams):
        return self.storage.object.create_bucket(data)

    def delete_bucket(self):
        return self.storage.object.del_bucket(self.bucket_id)

    def get_bucket(self):
        return self.storage.object.get_bucket(self.bucket_id)

    def list_objects(self, params: IPaginationParams):
        return self.storage.object.list(self.bucket_id, params)

    def get_object(self, object_id: str):
        return self.storage.object.get_object(self.bucket_id, object_id)

    def put_object(self, data: IObjectUploadParams):
        return self.storage.object.put_object(self.bucket_id, data)

    def delete_object(self, object_id: str):
        return self.storage.object.del_object(self.bucket_id, object_id)

    # Queue convenience methods with environment variables
    def list_queues(self, params: IPaginationParams):
        return self.storage.queue.list(params)

    def create_queue(self, data: IQueueCreateParams):
        return self.storage.queue.create(data)

    def get_queue(self, name: str):
        return self.storage.queue.get(name)

    def update_queue(self, data: IQueueUpdateParams):
        return self.storage.queue.update(data)

    def delete_queue(self):
        return self.storage.queue.delete(self.queue_id)

    def push_message(self, data: IQueuePushParams):
        return self.storage.queue.push(self.queue_id, data)

    def pull_message(self, limit: Optional[int] = None):
        return self.storage.queue.pull(self.queue_id, limit)

    def ack_message(self, msg_id: str):
        return self.storage.queue.ack(self.queue_id, msg_id)