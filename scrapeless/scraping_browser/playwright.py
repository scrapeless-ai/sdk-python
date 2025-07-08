import asyncio
from typing import Optional, Union, Any, Dict
from playwright.async_api import async_playwright, Browser, Page
from .base import BaseBrowser, create_logger
from ..types.browser import (
    PlaywrightLaunchOptions,
    CaptchaCDPResponse,
    LiveURLResponse,
    SetAutoSolveOptions,
    ImageToTextOptions,
    SetConfigOptions,
)
from ..types.config import ScrapelessConfig

logger = create_logger('Playwright')

class ScrapelessPlaywright(BaseBrowser):
    """
    Enhanced Playwright browser implementation using Scrapeless API
    Provides additional automation capabilities and browser control
    """
    def __init__(self):
        super().__init__()

    async def connect(self, config: Optional[Union[PlaywrightLaunchOptions, ScrapelessConfig]] = None) -> Browser:
        if config is None:
            config = PlaywrightLaunchOptions()
        config_for_init = config if isinstance(config, ScrapelessConfig) or config is None else None
        self._init_browser_service(config_for_init)
        if self.browser_service is None:
            raise RuntimeError("browser_service is not initialized. Failed to connect to browser.")
        browser_url = self.browser_service.create(config).browser_ws_endpoint
        p = await async_playwright().start()
        browser = await p.chromium.connect_over_cdp(browser_url)
        logger.info("Successfully connected to Scrapeless browser", {
            'sessionName': getattr(config, 'session_name', None)
        })
        return browser

    async def create_playwright_cdp_session(self, page: Page) -> Any:
        """
        Create a Scrapeless-enhanced CDP session with custom automation methods
        """
        cdp_session = await page.context.new_cdp_session(page)

        class ScrapelessCDPSession:
            def __init__(self, session, target_page):
                self._cdp = session
                self._page = target_page

            async def live_url(self) -> LiveURLResponse:
                try:
                    result = await self._cdp.send('Agent.liveURL')
                    return LiveURLResponse(error=result.get('error'), liveURL=result.get('liveURL'))
                except Exception as e:
                    logger.error('Error in liveURL', {'error': str(e)})
                    return LiveURLResponse(error=str(e), liveURL=None)

            async def real_click(self, selector: str) -> None:
                try:
                    await self._page.wait_for_selector(selector)
                    await self._cdp.send('Agent.click', {'selector': selector})
                    logger.debug('Successfully clicked element', {'selector': selector})
                except Exception as e:
                    logger.error('Error in realClick', {'selector': selector, 'error': str(e)})
                    raise RuntimeError(f'Failed to click element "{selector}": {str(e)}')

            async def real_fill(self, selector: str, text: str) -> None:
                try:
                    await self._page.wait_for_selector(selector)
                    await self._cdp.send('Agent.type', {'selector': selector, 'content': text})
                    logger.debug('Successfully filled element', {'selector': selector, 'textLength': len(text)})
                except Exception as e:
                    logger.error('Error in realFill', {'selector': selector, 'error': str(e)})
                    raise RuntimeError(f'Failed to type text into "{selector}": {str(e)}')

            async def set_auto_solve(self, options: SetAutoSolveOptions) -> None:
                try:
                    await self._cdp.send('Captcha.setAutoSolve', {
                        'autoSolve': options.autoSolve if options.autoSolve is not None else True,
                        'options': str(options.options) if options.options is not None else None
                    })
                    logger.debug('Auto-solve configured', {'options': options})
                except Exception as e:
                    logger.error('Error in setAutoSolve', {'options': options, 'error': str(e)})
                    raise RuntimeError(f'Failed to set auto solve: {str(e)}')

            async def disable_captcha_auto_solve(self) -> None:
                try:
                    await self._cdp.send('Captcha.setAutoSolve', {'autoSolve': False})
                    logger.debug('Auto-solve disabled')
                except Exception as e:
                    logger.error('Error in disableCaptchaAutoSolve', {'error': str(e)})
                    raise RuntimeError(f'Failed to disable captcha auto solve: {str(e)}')

            async def solve_captcha(self, options: Dict[str, Any] = None) -> CaptchaCDPResponse:
                if options is None:
                    options = {}
                solve_options = {'detectTimeout': options.get('timeout', 30000)}
                if 'options' in options:
                    solve_options['options'] = str(options['options'])
                try:
                    result = await self._cdp.send('Captcha.solve', solve_options)
                    logger.debug('Captcha solve attempt completed', {'result': result})
                    return CaptchaCDPResponse(**result)
                except Exception as e:
                    logger.error('Error in solveCaptcha', {'options': options, 'error': str(e)})
                    raise RuntimeError(f'Failed to solve captcha: {str(e)}')

            async def image_to_text(self, params: ImageToTextOptions) -> None:
                timeout = params.timeout if params.timeout is not None else 30000
                logger.debug(f'Waiting for captcha solved with timeout: {timeout}ms')
                try:
                    await self._cdp.send('Captcha.imageToText', params.__dict__)
                except Exception as e:
                    logger.error('Error in imageToText', {'params': params, 'error': str(e)})
                    raise RuntimeError(f'Failed to solve image captcha: {str(e)}')

            async def set_config(self, options: SetConfigOptions) -> None:
                try:
                    await self._cdp.send('Captcha.setConfig', {'config': str(options)})
                    logger.debug('Set config success', {'options': options})
                except Exception as e:
                    logger.error('Error in setConfig', {'options': options, 'error': str(e)})
                    raise RuntimeError(f'Failed to set auto solve: {str(e)}')

        return ScrapelessCDPSession(cdp_session, page)

# Singleton instance for convenient access
Playwright = ScrapelessPlaywright()