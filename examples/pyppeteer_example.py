"""
Example: Using Scrapeless SDK's Pyppeteer Integration

This example demonstrates how to use the Pyppeteer class for browser automation
including page navigation and extended CDP session methods.
NOTE: You need to have `pyppeteer` installed to run this example.
"""
from scrapeless import Logger
from scrapeless.scraping_browser import ScrapelessPyppeteer as Pyppeteer
from scrapeless.types import PyppeteerLaunchOptions
from time import sleep

def pyppeteer_example() -> None:
    """
    Main function to demonstrate Pyppeteer browser automation synchronously.
    """
    import asyncio
    logger = Logger().with_prefix('pyppeteer-example')
    async def _run() -> None:
        logger.debug('Starting browser...')
        client = Pyppeteer()
        # Launch browser instance
        config = PyppeteerLaunchOptions(
            session_name='sdk-pyppeteer-example',
            session_ttl=180,
            proxy_country='US',
            session_recording=True,
            defaultViewport=None
        )
        browser = await client.connect(config=config)
        try:
            logger.debug('Creating new page...')
            # Create a new page
            page = await browser.newPage()
            logger.debug('Creating CDP session with extended methods...')
            await page.goto('https://www.google.com/', {'waitUntil': 'networkidle0'})
            # Use Pyppeteer instance to create CDP session

            cdp_session = await client.create_pyppeteer_cdp_session(page)
            await cdp_session.disable_captcha_auto_solve()
            await page.goto('https://prenotami.esteri.it/')
            email = 'xxxxxxx@gmail.com'
            password = 'xxxx'
            sleep(10_000)
            logger.debug('Filling form using CDP methods...')
            await cdp_session.real_fill('#login-email', email)
            await cdp_session.real_fill('#login-password', password)
            sleep(5_000)
            logger.debug('Solving captcha...')
            captcha = await cdp_session.solve_captcha()
            if captcha['success']:
                logger.info(f'Captcha detected: {captcha}')
            else:
                logger.error(f"Failed to detect captcha: {captcha['message']}")
                return
            # await cdp_session.real_click('button[type="submit"]')
            sleep(10_000)
        except Exception as error:
            print(f'Error running example: {error}')
        finally:
            if browser:
                logger.debug('Closing browser...')
                await browser.close()
    asyncio.get_event_loop().run_until_complete(_run())

def run_example() -> None:
    """
    Main entry for running the Pyppeteer example.
    """
    pyppeteer_example()
    print('Pyppeteer example completed.')

run_example() 