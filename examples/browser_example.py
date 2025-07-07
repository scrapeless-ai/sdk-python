"""
Example: Demonstrating how to use the Scrapeless SDK browser module
Filename: browser-example.py
"""
from scrapeless import Scrapeless
from scrapeless.types import ICreateBrowser
import pyppeteer

def browser_example() -> None:
    """
    Main function to demonstrate how to create a browser session and navigate to a website synchronously.
    """
    import asyncio
    async def _run() -> None:
        try:
            # Initialize the client with API key from environment
            client = Scrapeless()
            print('Creating browser session...')
            # Create browser session and get WebSocket endpoint
            config = ICreateBrowser(
                session_name='sdk_test',
                session_ttl=180,
                proxy_country='US',
                session_recording=True
            )
            session = client.browser.create(config).__dict__
            browser_ws_endpoint = session['browser_ws_endpoint']
            print('Browser WebSocket endpoint created:', browser_ws_endpoint)
            # Connect to browser using pyppeteer
            browser = await pyppeteer.connect({ 'browserWSEndpoint': browser_ws_endpoint })
            # Open new page and navigate to website
            page = await browser.newPage()
            await page.goto('https://www.scrapeless.com')
            print('Page title:', await page.title())
            # Take screenshot
            await page.screenshot({'path': './browser-example.png', 'fullPage': True})
            # Close browser
            await browser.close()
            print('Example completed successfully')
        except Exception as error:
            print('Example error:', error)
    asyncio.get_event_loop().run_until_complete(_run())

def run_example() -> None:
    """
    Main entry for running the browser example.
    """
    browser_example()
    print('Browser example completed.')

run_example() 