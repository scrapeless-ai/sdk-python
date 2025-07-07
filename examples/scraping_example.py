"""
Example: Demonstrating how to use the Scrapeless SDK scraping module
Filename: scraping_example.py
"""
import time
from scrapeless import Scrapeless, Logger
from scrapeless.types import ScrapingTaskRequest

request = ScrapingTaskRequest(
    actor='scraper.google.search',
    input={'q': 'nike site:www.nike.com'}
)
def google_search_example() -> None:
    """
    Example for creating a scraping task and polling for the result synchronously.
    """
    task = client.scraping.create_task(request=request)
    if task['status'] == 200:
        print('Task result:', task['data'])
        return
    while True:
        time.sleep(1)
        result = client.scraping.get_task_result(task['data']['taskId'])
        if result['status'] == 200:
            print('Polled result:', result['data'])
            return

def google_search_by_scrape_example() -> None:
    """
    Example for using the scraping scrape method synchronously.
    """
    result = client.scraping.scrape(request=request)
    print('Scrape result:', result)

def run_example() -> None:
    """
    Main entry for running all scraping examples.
    """
    try:
        google_search_example()
    except Exception as e:
        Log.error(f'google_search_example error: {e}')
    try:
        google_search_by_scrape_example()
    except Exception as e:
        Log.error(f'google_search_by_scrape_example error: {e}')
    print('Scraping example completed.')

Log = Logger().with_prefix('Scraping Example')
client = Scrapeless()

run_example()