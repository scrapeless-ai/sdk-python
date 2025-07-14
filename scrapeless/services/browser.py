from dataclasses import asdict
from typing import Optional
from .base import BaseService
from .extension import ExtensionService
from ..error import ScrapelessError
from ..env import get_env_with_default
from ..types.browser import ICreateBrowser, ICreateBrowserResponse
from urllib.parse import urlencode
import json

DEFAULT_BROWSER_OPTIONS = ICreateBrowser(
    session_name='',
    session_ttl=180,
    proxy_country='ANY'
)

class BrowserService(BaseService):
    def __init__(self, api_key: str, base_url: str, timeout: int = 30000):
        super().__init__(api_key, base_url, timeout)
        base_api_url = get_env_with_default('SCRAPELESS_BASE_API_URL', 'https://api.scrapeless.com')
        self.extension = ExtensionService(api_key, base_api_url, timeout)

    def create(self, options: Optional[ICreateBrowser] = None) -> ICreateBrowserResponse:
        # Merge default options with user provided options
        if options is None:
            data = DEFAULT_BROWSER_OPTIONS
        else:
            data = DEFAULT_BROWSER_OPTIONS
            payload = asdict(options)
            for k, v in payload.items():
                if v is not None:
                    setattr(data, k, v)
        params = {
            'token': self.api_key,
            'session_name': data.session_name,
            'session_ttl': str(data.session_ttl) if data.session_ttl else '',
            'session_recording': str(data.session_recording) if data.session_recording is not None else '',
            'proxy_country': data.proxy_country,
            'proxy_url': data.proxy_url,
            'fingerprint': str(data.fingerprint) if data.fingerprint else '',
            'extension_ids': data.extension_ids
        }
        if data.proxy_url:
            params.pop('proxy_country', None)
        filtered_params = {k: v for k, v in params.items() if v not in (None, '')}
        search = urlencode(filtered_params)
        protocol = 'wss' if self.base_url.startswith('https://') else 'ws'
        return ICreateBrowserResponse(
            browser_ws_endpoint=f"{protocol}://{self.base_url.replace('https://', '').replace('http://', '')}/browser?{search}"
        )

    async def create_async(self, options: Optional[ICreateBrowser] = None) -> ICreateBrowserResponse:
        return self.create(options)

    async def create_session(self, options: Optional[ICreateBrowser] = None) -> ICreateBrowserResponse:
        if options is None:
            data = DEFAULT_BROWSER_OPTIONS
        else:
            data = DEFAULT_BROWSER_OPTIONS
            payload = asdict(options)
            for k, v in payload.items():
                if v is not None:
                    setattr(data, k, v)
        params = {
            'token': self.api_key,
            'session_name': data.session_name if data.session_name else '',
            'session_ttl': str(data.session_ttl) if data.session_ttl else '',
            'session_recording': str(data.session_recording) if data.session_recording is not None else '',
            'proxy_country': data.proxy_country if data.proxy_country else 'ANY',
            'proxy_url': data.proxy_url if data.proxy_url else '',
            'fingerprint': str(data.fingerprint) if data.fingerprint else '',
            'extension_ids': data.extension_ids if data.extension_ids is not None else ''
        }
        if data.proxy_url:
            params.pop('proxy_country', '')

        query_str = urlencode(params)

        try:
            task = self.request(f"/browser?{query_str}", "GET", response_with_status=True)

            if not task['data']['success']:
                ScrapelessError(f"Failed to create browser session: ${json.dumps(task.data)}")

            if not task['data']['taskId']:
                ScrapelessError('Failed to create browser session: taskId is missing')

            return ICreateBrowserResponse(
                browser_ws_endpoint=f"wss://browser.scrapeless.com/browser/{task['data']['taskId']}?token={self.api_key}"
            )
        except Exception as e:
            print(e)
            ScrapelessError(f"Failed to create browser session: ${e}")
            return ICreateBrowserResponse(
                browser_ws_endpoint=''
            )