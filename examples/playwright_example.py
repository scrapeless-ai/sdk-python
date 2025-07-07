"""
Example: Using Scrapeless SDK's Playwright Integration

This example demonstrates how to use the Playwright class for browser automation
including page navigation and extended page methods.
"""
from scrapeless import Logger
from scrapeless.scraping_browser import ScrapelessPlaywright as Playwright
from scrapeless.types import PlaywrightLaunchOptions
from time import sleep

def playwright_example() -> None:
    """
    Main function to demonstrate Playwright browser automation synchronously.
    """
    logger = Logger().with_prefix('playwright-example')
    async def _run() -> None:
        logger.debug('Starting browser...')
        # Launch browser instance
        client = Playwright()
        config = PlaywrightLaunchOptions(
            session_name='sdk-playwright-example',
            session_ttl=180,
            proxy_country='US',
            session_recording=True,
            defaultViewport=None
        )
        browser = await client.connect(config=config)
        try:
            context = browser.contexts[0]
            logger.debug('Creating new page...')
            # Create a new page
            page = await context.new_page()
            cdp_session = await client.create_playwright_cdp_session(page)
            await page.goto('https://google.com/')
            await cdp_session.disable_captcha_auto_solve()
            # Navigate to target website
            logger.debug('Navigating to target website...')
            await page.goto('https://prenotami.esteri.it/')
            # Wait for page to load
            await page.wait_for_load_state('networkidle')
            live_url = await cdp_session.live_url()
            if live_url.error:
                logger.error(f'Failed to get current page URL: {live_url.error}')
            else:
                logger.info(f'Current page URL: {live_url}')
            email = 'xxx.mel@yqdfw.org'
            password = 'xxx*'
            await page.wait_for_selector('#login-email')
            await page.wait_for_selector('#login-password')
            sleep(10_000)
            await cdp_session.real_fill('#login-email', email)
            await cdp_session.real_fill('#login-password', password)
            # Wait to observe the result
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
    import asyncio
    asyncio.get_event_loop().run_until_complete(_run())

def run_example() -> None:
    """
    Main entry for running the Playwright example.
    """
    playwright_example()
    print('Playwright example completed.')

run_example() 