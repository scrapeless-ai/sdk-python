"""
Example: Demonstrating how to use Actor storage methods with environment variables
This simulates the environment in which your Actor would run
"""
import os
import json
from datetime import datetime, timedelta
from scrapeless import Actor
from scrapeless.types import IPaginationParams, IKVValueData, IQueuePushParams

# Mock environment variables for testing
# In a real Actor runtime, these would be set by the platform
os.environ['SCRAPELESS_INPUT'] = json.dumps({
    'keywords': ['apple', 'banana', 'orange'],
    'maxResults': 10
})
os.environ['SCRAPELESS_DATASET_ID'] = 'mock_dataset_id'
os.environ['SCRAPELESS_KV_NAMESPACE_ID'] = 'mock_kv_namespace_id'
os.environ['SCRAPELESS_BUCKET_ID'] = 'mock_bucket_id'
os.environ['SCRAPELESS_QUEUE_ID'] = 'mock_queue_id'


def run_actor_example():
    try:
        print('Starting Actor storage example')

        # Initialize Actor
        actor = Actor()

        # Get input data from environment
        input_data = actor.input()
        print('Actor input:', input_data)

        # Dataset operations
        print('\n--- Dataset operations ---')
        try:
            # Get dataset ID from environment
            dataset_id = os.getenv('SCRAPELESS_DATASET_ID')

            # Add items to dataset (using Actor convenience method)
            items = [{'keyword': keyword, 'timestamp': datetime.now().isoformat()} for keyword in input_data['keywords']]
            add_result = actor.add_items(items)
            print('Added items to dataset:', add_result)

            # Get items from dataset (using Actor convenience method)
            pagination = IPaginationParams(
                page=1,
                page_size=10,
            )
            get_result = actor.get_items(pagination)
            print('Items from dataset:', get_result)

            # Using direct storage service
            # Note: In a real environment, the results would match. Here we can't truly compare.
            print(f'Would use direct API call with dataset_id: {dataset_id}')

        except Exception as e:
            print(f'Dataset operations error: {e}')

        # KV storage operations
        print('\n--- KV storage operations ---')
        try:
            # Get KV namespace ID from environment
            namespace_id = os.getenv('SCRAPELESS_KV_NAMESPACE_ID')

            # Set value (using Actor convenience method)
            data = IKVValueData(
                key='last_run',
                value=datetime.now().isoformat()
            )
            set_value = actor.set_value(data)
            print('Set KV value:', set_value)

            # Get value (using Actor convenience method)
            get_value = actor.get_value('last_run')
            print('Get KV value:', get_value)
            
            print(f'Would use direct API call with namespace_id: {namespace_id}')

        except Exception as e:
            print(f'KV storage operations error: {e}')

        # Queue operations
        print('\n--- Queue operations ---')
        try:
            # Get queue ID from environment
            queue_id = os.getenv('SCRAPELESS_QUEUE_ID')

            # Push message to queue (using Actor convenience method)
            deadline = datetime.now() + timedelta(hours=1)
            push_params = IQueuePushParams(
                name='product-next',
                payload=json.dumps({'a': 'a'}),
                retry=2,
                timeout=3000,
                deadline=deadline
            )
            push_result = actor.push_message(push_params)
            print('Pushed message to queue:', push_result)

            # Pull message from queue (using Actor convenience method)
            pull_result = actor.pull_message()
            print('Pulled message from queue:', pull_result)

            # Acknowledge message (using Actor convenience method)
            if pull_result and len(pull_result) > 0:
                ack_result = actor.ack_message(pull_result[0]['id'])
                print('Acknowledged message:', ack_result)
            
            print(f'Would use direct API call with queue_id: {queue_id}')

        except Exception as e:
            print(f'Queue operations error: {e}')

    except Exception as e:
        print(f'Actor example error: {e}')


# Run the example
run_actor_example()