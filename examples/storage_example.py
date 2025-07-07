"""
Example: Demonstrating how to use the Scrapeless SDK storage module
Filename: storage-example.py
"""
import os
import json
from datetime import datetime, timedelta
from scrapeless import Scrapeless
from scrapeless.types import (
    IPaginationParams,
    IDatasetListParams,
    IKVValueData,
    IQueueCreateParams,
    IQueuePushParams
)

def dataset_example(client):
    """
    Demonstrates how to create and use the dataset storage
    """
    try:
        print('Dataset example:')

        dataset = client.storage.dataset.create_dataset('products-price')
        print(f"Dataset created with ID: {dataset['id']}")

        # Add items to the dataset
        client.storage.dataset.add_items(dataset['id'], [
            {'name': 'Product 1', 'price': 19.99, 'category': 'Electronics'},
            {'name': 'Product 2', 'price': 29.99, 'category': 'Home'},
            {'name': 'Product 3', 'price': 9.99, 'category': 'Clothing'}
        ])
        print('Items added to dataset')

        # Get items from the dataset
        params = IDatasetListParams(page=1, page_size=10)
        items = client.storage.dataset.list_datasets(params)
        print('Dataset items:', items)

        print('Dataset example completed\n')
    except Exception as error:
        print('Dataset example error:', error)

def kv_storage_example(client):
    """
    Demonstrates how to create and use the key-value storage
    """
    try:
        print('Key-Value storage example:')

        # Create a new KV namespace
        namespace = client.storage.kv.create_namespace('config-list')
        print(f"KV namespace created with ID: {namespace['id']}")

        # Set values in the namespace
        data = IKVValueData(key='config', value=json.dumps({'features': {'darkMode': True}}))
        client.storage.kv.set_value(namespace['id'], data)
        print('Value set in KV store')

        # Get value from the namespace
        config = client.storage.kv.get_value(namespace['id'], 'config')
        print('Retrieved config:', json.loads(config))

        # List keys in the namespace
        params = IPaginationParams(page=1, page_size=10)
        keys = client.storage.kv.list_keys(namespace['id'], params)
        print('KV store keys:', keys)

        print('KV storage example completed\n')
    except Exception as error:
        print('KV storage example error:', error)

def object_storage_example(client):
    """
    Demonstrates how to create and use the object storage
    """
    try:
        print('Object storage example:')

        # Create a new bucket
        bucket = client.storage.object.create_bucket(
            name='images-bucket',
            description='Storage for product images'
        )
        print(f"Object bucket created with ID: {bucket['id']}")

        # Upload a file to the bucket (in a real scenario, you would use a real file path)
        # Note: The Python SDK expects the file content, not a path.
        # For this example, we'll simulate file content.
        with open('sample-image.jpg', 'wb') as f:
            f.write(b"fake image data")
            
        upload_result = client.storage.object.put(
            file='sample-image.jpg'
        )
        print('File uploaded to object storage:', upload_result)
        os.remove('sample-image.jpg')

        # List objects in the bucket
        objects = client.storage.object.list(page=1, page_size=10)
        print('Objects in bucket:', objects)

        print('Object storage example completed\n')
    except Exception as error:
        print('Object storage example error:', error)

def queue_storage_example(client):
    """
    Demonstrates how to create and use the queue storage
    """
    try:
        print('Queue storage example:')

        # Create a new queue
        data = IQueueCreateParams(
            name='product-queue',
            actor_id='123',
            run_id='123',
            description='Product queue'
        )
        queue = client.storage.queue.create(data)
        print(f"Queue created with ID: {queue['id']}")

        # Push messages to the queue
        deadline = datetime.now() + timedelta(hours=1)
        push_params = IQueuePushParams(
            name='product-next',
            payload=json.dumps({'a': 'a'}),
            retry=2,
            timeout=3000,
            deadline=deadline
        )
        message1 = client.storage.queue.push(queue['id'], params=push_params)
        print('Message pushed to queue:', message1)

        # Pull messages from the queue
        messages = client.storage.queue.pull(queue['id'], 10)
        print('Messages pulled from queue:', messages)

        # Acknowledge a message (if any)
        if messages and len(messages) > 0:
            client.storage.queue.ack(queue['id'], messages[0]['id'])
            print(f"Message {messages[0]['id']} acknowledged")

        print('Queue storage example completed\n')
    except Exception as error:
        print('Queue storage example error:', error)

def run_example():
    """
    Main example function
    """
    try:
        # Initialize the Scrapeless client
        client = Scrapeless()

        # Run the examples
        dataset_example(client)
        kv_storage_example(client)
        # object_storage_example(client)
        queue_storage_example(client)

        print('All storage examples completed successfully')
    except Exception as error:
        print('Example error:', error)

# Run the example
run_example()