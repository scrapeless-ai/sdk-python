"""
Scrapeless Python SDK - Universal Service Example
"""
import asyncio
from scrapeless import Universal, Logger
from scrapeless.types import (
    UniversalScrapingRequest,
    UniversalJsRenderInput,
    UniversalWebUnlockerInput,
)

log = Logger().with_prefix('universal-example')
universal = Universal()

def js_render_example() -> None:
    """
    js render example
    """
    try:
        log.info('Start JS render example...')
        js_input = UniversalJsRenderInput(
            url='https://www.scrapeless.com',
            headless=False,
            js_render=True,
            js_instructions=[
                {'wait': 10000},
                {'wait_for': ['.dynamic-content', 30000]},
                {'click': ['#load-more', 1000]},
                {'fill': ['#search-input', 'search term']},
                {'keyboard': ['press', 'Enter']},
                {'evaluate': 'window.scrollTo(0, document.body.scrollHeight)'}
            ],
            block={
                'resources': [
                    'stylesheet', 'image', 'media', 'font', 'script', 'texttrack',
                    'xhr', 'fetch', 'eventsource', 'websocket', 'manifest', 'other'
                ]
            }
        )
        req = UniversalScrapingRequest(
            actor='unlocker.webunlocker',
            input=js_input,
        )
        result = universal.js_render(req)
        log.info(f'JS render result: {result}')
    except Exception as error:
        log.error(f'JS render example error: {error}')

def web_unlocker_example() -> None:
    """
    Web Unlocker example
    """
    try:
        log.info('Start Web Unlocker example...')
        req = UniversalScrapingRequest(
            actor='unlocker.webunlocker',
            input=UniversalWebUnlockerInput(
                url='https://www.nike.com/ca/launch?s=upcoming',
                type='',
                redirect=False,
                method='GET',
                header={
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
                }
            )
        )
        result = universal.web_unlocker(req)
        log.info(f'Web Unlocker result: {result}')
    except Exception as error:
        log.error(f'Web Unlocker example error: {error}')

def run_example() -> None:
    """
    Main entry, run all universal examples in sequence
    """
    try:
        js_render_example()
        web_unlocker_example()
        log.info('All Universal examples completed')
    except Exception as error:
        log.error(f'Universal example error: {error}')

run_example()