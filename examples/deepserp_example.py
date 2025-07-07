"""
Example: Demonstrating how to use the Scrapeless SDK DeepSERP module
Filename: deepserp_example.py
"""
import os
import time
from scrapeless import Scrapeless, Logger
from scrapeless.types import ScrapingTaskRequest

log = Logger().with_prefix('Deepserp')
api_key = os.getenv('SCRAPELESS_API_KEY') or 'your_api_key_here'
client = Scrapeless({
    'api_key': api_key,
})

def google_search_example() -> None:
    """
    Example for creating a DeepSERP task and polling for the result synchronously.
    """
    request = ScrapingTaskRequest(
        actor='scraper.google.search',
        input={'q': 'nike site:www.nike.com'}
    )
    task = client.deepserp.create_task(request)
    if task['status'] == 200:
        print('Task result:', task['data'])
        return
    while True:
        time.sleep(1)
        result = client.deepserp.get_task_result(task['data']['taskId'])
        if result['status'] == 200:
            print('Polled result:', result['data'])
            return

def google_search_by_scrape_example() -> None:
    """
    Example for using the DeepSERP scrape method synchronously.
    """
    request = ScrapingTaskRequest(
        actor='scraper.google.search',
        input={'q': 'nike site:www.nike.com'}
    )
    result = client.deepserp.scrape(request)
    print('Scrape result:', result)

def run_example() -> None:
    """
    Main entry for running all DeepSERP examples.
    """
    try:
        google_search_example()
    except Exception as e:
        log.error(f'google_search_example error: {e}')
    try:
        google_search_by_scrape_example()
    except Exception as e:
        log.error(f'google_search_by_scrape_example error: {e}')
    print('DeepSERP example completed.')

run_example() 