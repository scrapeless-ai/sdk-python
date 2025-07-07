"""
Scrapeless Python SDK - Extension Service Example
NOTE: You need to have `pyppeteer` installed to run this example.
"""
import os
import zipfile
from scrapeless import Scrapeless
import pyppeteer
from typing import Any, Dict

def create_dummy_extension_zip(file_path: str) -> None:
    """Creates a dummy zip file for testing."""
    with zipfile.ZipFile(file_path, 'w') as zf:
        zf.writestr('manifest.json', '{"name": "Dummy Extension", "version": "1.0", "manifest_version": 2}')

def extension_example() -> None:
    """
    Main function to demonstrate extension upload, update, list, get, use, and delete synchronously.
    """
    import asyncio
    api_key = os.getenv('SCRAPELESS_API_KEY') or 'your_api_key_here'
    client = Scrapeless({
        'api_key': api_key,
    })
    scraping_browser = client.browser

    async def _run() -> None:
        try:
            print('=== Scrapeless Browser Extension Tests ===\n')
            # Upload a new extension
            dummy_file = 'dummy_extension.zip'
            create_dummy_extension_zip(dummy_file)
            uploaded = await scraping_browser.extension.upload(dummy_file, 'Scrapeless')
            os.remove(dummy_file)
            print('Uploaded extension:', uploaded)
            print('\n')
            if uploaded and uploaded.get('id'):
                extension_id = uploaded['id']
                # List all extensions
                response = await scraping_browser.extension.list()
                print('Extension list:', response)
                print('\n')
                # Get details of a specific extension
                response = await scraping_browser.extension.get(extension_id)
                print('Extension details:', response)
                print('\n')
                # Update the extension
                dummy_file_updated = 'dummy_extension_updated.zip'
                create_dummy_extension_zip(dummy_file_updated)
                response = await scraping_browser.extension.update(extension_id, dummy_file_updated, 'Scrapeless')
                os.remove(dummy_file_updated)
                print('Extension updated:', response)
                print('\n')
                # Use the extension in a new browser session
                session = scraping_browser.create({
                    'session_name': 'use-extension',
                    'session_ttl': 180,
                    'session_recording': True,
                    'extension_ids': [extension_id]
                })
                browser_ws_endpoint = session['browserWSEndpoint']
                browser = await pyppeteer.connect(
                    browserWSEndpoint=browser_ws_endpoint,
                    defaultViewport=None
                )
                page = await browser.newPage()
                await page.goto('https://example.com')
                await browser.close()
                print('Used extension in browser session.')
                print('\n')
                # Delete the extension
                response = await scraping_browser.extension.delete(extension_id)
                print('Extension deleted:', response)
                print('\n')
            print('🎉 All extension tests completed successfully')
        except Exception as error:
            print(f'❌ Extension tests failed with error: {error}')
    asyncio.get_event_loop().run_until_complete(_run())

def run_example() -> None:
    """
    Main entry for running the extension example.
    """
    extension_example()
    print('Extension example completed.')

run_example() 