"""
Complete Actor Usage Example
Demonstrates how to use various features of the Actor class in English only.
"""
import os
import json
from datetime import datetime, timedelta
from scrapeless import Actor
from typing import Any, Dict
from scrapeless.types import IPaginationParams, IKVValueData, IQueuePushParams

# Mock environment variables - in a real Actor runtime, these would be set by the platform
os.environ['SCRAPELESS_ACTOR_ID'] = 'act_12345'
os.environ['SCRAPELESS_RUN_ID'] = 'run_67890'
os.environ['SCRAPELESS_USER_ID'] = 'user_12345'
os.environ['SCRAPELESS_TEAM_ID'] = 'team_12345'
os.environ['SCRAPELESS_API_KEY'] = 'your_api_key_here'
os.environ['SCRAPELESS_DATASET_ID'] = 'dat_12345'
os.environ['SCRAPELESS_KV_NAMESPACE_ID'] = 'ns_12345'
os.environ['SCRAPELESS_BUCKET_ID'] = 'buck_12345'
os.environ['SCRAPELESS_QUEUE_ID'] = 'q_12345'
os.environ['SCRAPELESS_INPUT'] = json.dumps({
    'url': 'https://example.com',
    'maxResults': 10,
    'keywords': ['apple', 'banana', 'orange'],
    'useProxy': True,
    'captcha': {
        'enabled': True,
        'type': 'recaptcha'
    },
    'options': {
        'headless': False,
        'screenshot': True,
        'waitTime': 5000
    }
})

def actor_full_example() -> None:
    """
    Main function to run the complete Actor example synchronously for demonstration.
    """
    print('Starting Actor example execution')
    try:
        # 1. Initialize Actor
        actor = Actor()
        print('Actor initialized')

        # 2. Get input data
        input_data: Dict[str, Any] = actor.input()
        print('Actor input data:', input_data)

        # 3. Dataset operations
        print('\n--- Dataset Operations ---')
        try:
            # Add items to dataset
            items = [{
                'keyword': keyword,
                'url': input_data['url'],
                'timestamp': datetime.now().isoformat()
            } for keyword in input_data['keywords']]
            add_result = actor.add_items(items)
            print('Added data to dataset:', add_result)
            pagination = IPaginationParams(
                page=1,
                page_size=10
            )
            get_result = actor.get_items(pagination)
            print('Retrieved data from dataset:', get_result)
            print('Using underlying API to operate on datasets')
            actor.storage.dataset.create_dataset('New Dataset')
        except Exception as e:
            print(f'Dataset operations error: {e}')

        # 4. KV storage operations
        print('\n--- KV Storage Operations ---')
        try:
            data = IKVValueData(
                key='last_run',
                value=datetime.now().isoformat()
            )
            actor.set_value(data)
            print('Set KV value successfully')
            last_run = actor.get_value('last_run')
            print('Retrieved KV value:', last_run)
            next_data = IKVValueData(
                key='config',
                value=json.dumps(input_data['options'])
            )
            actor.set_value(next_data)
            config_str = actor.get_value('config')
            config = json.loads(config_str)
            print('Parsed configuration:', config)
        except Exception as e:
            print(f'KV storage operations error: {e}')

        # 5. Object storage operations
        print('\n--- Object Storage Operations ---')
        try:
            print('Object storage operations example (for use in real environment)')
            # See commented code for real usage
        except Exception as e:
            print(f'Object storage operations error: {e}')

        # 6. Queue operations
        print('\n--- Queue Operations ---')
        try:
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
            pull_result = actor.pull_message()
            print('Pulled message from queue:', pull_result)
            if pull_result and len(pull_result) > 0:
                ack_result = actor.ack_message(pull_result[0]['id'])
                print('Acknowledged message completion:', ack_result)
        except Exception as e:
            print(f'Queue operations error: {e}')

        # 7. Browser automation
        print('\n--- Browser Automation ---')
        try:
            print('In a real environment, this would create a browser session for automation')
            # See commented code for real usage
        except Exception as e:
            print(f'Browser automation error: {e}')

        # 8. CAPTCHA solving
        print('\n--- CAPTCHA Solving ---')
        try:
            if input_data.get('captcha', {}).get('enabled'):
                print('In a real environment, this would handle CAPTCHA')
                # See commented code for real usage
        except Exception as e:
            print(f'CAPTCHA solving error: {e}')

        # 9. Proxy usage
        print('\n--- Proxy Usage ---')
        try:
            if input_data.get('useProxy'):
                print('In a real environment, this would obtain and use proxies')
                # See commented code for real usage
        except Exception as e:
            print(f'Proxy usage error: {e}')

        # 10. Event handling
        print('\n--- Event Handling ---')
        print("Actor execution finished. In a real environment, the platform handles shutdown events.")
    except Exception as e:
        print(f'Actor example error: {e}')

def run_example() -> None:
    """
    Main entry for running the complete actor example.
    """
    actor_full_example()
    print('Actor full example completed.')

run_example() 