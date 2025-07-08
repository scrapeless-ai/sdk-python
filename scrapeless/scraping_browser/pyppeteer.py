from typing import Optional, Union, Any, Dict
from pyppeteer import connect, browser, page
from .base import BaseBrowser, create_logger
from ..types.browser import (
    PyppeteerLaunchOptions,
    CaptchaCDPResponse,
    LiveURLResponse,
    SetAutoSolveOptions,
    ImageToTextOptions,
    SetConfigOptions
)
from ..types.config import ScrapelessConfig

logger = create_logger('Pyppeteer')

class ScrapelessPyppeteer(BaseBrowser):
    """
    Enhanced Scrapeless Pyppeteer browser implementation using Scrapeless API
    """
    def __init__(self):
        super().__init__()

    async def connect(self, config: Optional[Union[PyppeteerLaunchOptions, ScrapelessConfig]] = None) -> browser:
        if config is None:
            config = PyppeteerLaunchOptions()
        config_for_init = config if isinstance(config, ScrapelessConfig) or config is None else None
        self._init_browser_service(config_for_init)
        browser_url = self.browser_service.create(config).browser_ws_endpoint
        handle_browser = await connect({ 'browserWSEndpoint': browser_url})
        return handle_browser

    @staticmethod
    async def create_pyppeteer_cdp_session(handle_page: page) -> Any:
        """
        Create a Scrapeless-enhanced CDP session with custom automation methods
        """
        cdp_session = await handle_page.target.createCDPSession()
        class ScrapelessCDPSession:
            def __init__(self, session, target_page):
                self._cdp = session
                self._page = target_page

            async def livr_url(self) -> LiveURLResponse:
                try:
                    result = await self._cdp.send('Agent.liveURL')
                    return LiveURLResponse(error=result.get('error'), liveURL=result.get('liveURL'))
                except Exception as e:
                    logger.error('Error in liveURL', {'error': str(e)})
                    return LiveURLResponse(error=str(e), liveURL=None)

            async def real_click(self, selector: str) -> None:
                try:
                    await self._page.waitForSelector(selector)
                    await self._cdp.send('Agent.click', {'selector': selector})
                    logger.debug('Successfully clicked element', {'selector': selector})
                except Exception as e:
                    logger.error('Error in realClick', {'selector': selector, 'error': str(e)})
                    raise RuntimeError(f'Failed to click element "{selector}": {str(e)}')

            async def real_fill(self, selector: str, text: str) -> None:
                try:
                    await self._page.waitForSelector(selector)
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

        return ScrapelessCDPSession(cdp_session, handle_page)

# Singleton instance for convenient access
Pyppeteer = ScrapelessPyppeteer()