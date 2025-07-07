"""
Scrapeless Python SDK - ScrapingCrawl Service Examples
This example demonstrates how to use the ScrapingCrawl SDK for scraping, crawling.
"""
import asyncio
import json
from scrapeless import ScrapingCrawl

def save_object_to_json(obj, filename):
    """
    Utility function to save an object to a JSON file.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(obj, f, indent=2, ensure_ascii=False)
        print(f'File saved successfully: {filename}')
    except Exception as e:
        print(f'Error saving file: {e}')

# Shared ScrapingCrawl instance
client = ScrapingCrawl({
    'api_key': 'your_api_key_here',
})

async def example_scrape():
    """
    Example: Scrape a single URL and save the result.
    """
    try:
        scrape_response = await client.scrape_url('https://example.com/', {
            'formats': ['markdown', 'html', 'links', 'screenshot@fullPage']
        })
        if scrape_response:
            save_object_to_json(scrape_response, 'scrapeless-demo-scrape.json')
            print(scrape_response)
    except Exception as error:
        print(f'❌ Scrape example failed: {error}')

async def example_batch_scrape():
    """
    Example: Scrape a single URL and save the result.
    """
    try:
        scrape_response = await client.batch_scrape_urls(['https://example.com/', 'https://example.com/'], {
            'formats': ['markdown', 'html', 'links', 'screenshot@fullPage'],
            'browserOptions': {
                'session_name': 'scrapingCrawl_batchScrape'
            }
        })
        if scrape_response:
            print(scrape_response)
    except Exception as error:
        print(f'❌ Scrape example failed: {error}')

async def example_crawl():
    """
    Example: Crawl a URL with specific options and save the result.
    """
    try:
        crawl_result = await client.crawl_url('https://example.com/', {
            'limit': 3,
            'maxDepth': 1,
            'scrapeOptions': {
                'formats': ['markdown', 'links', 'html', 'screenshot@fullPage']
            }
        })
        if crawl_result:
            save_object_to_json(crawl_result, 'scrapeless-demo-crawl.json')
            print(crawl_result)
    except Exception as error:
        print(f'❌ Crawl example failed: {error}')

async def run_examples():
    """
    Run all ScrapingCrawl examples sequentially.
    """
    print('=== Scrapeless ScrapingCrawl Service Examples ===\n')
    await example_scrape()
    print('\n')
    await example_batch_scrape()
    print('\n')
    await example_crawl()
    print('\n')
    print('🎉 All examples completed')

# Run the examples
if __name__ == '__main__':
    asyncio.run(run_examples()) 