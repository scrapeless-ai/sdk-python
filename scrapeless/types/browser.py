from dataclasses import dataclass
from typing import Optional, Any, Dict, List, Callable, TypeVar, Generic

"""
Browser session creation options
"""
@dataclass
class ICreateBrowser:
    session_name: Optional[str] = None
    session_ttl: Optional[int] = None
    session_recording: Optional[bool] = None
    proxy_country: Optional[str] = None
    proxy_url: Optional[str] = None
    fingerprint: Optional[dict] = None
    extension_ids: Optional[str] = None

"""
Browser session creation response
"""
@dataclass
class ICreateBrowserResponse:
    browser_ws_endpoint: str

"""
Base interface for browser launch options
"""
@dataclass
class BaseLaunchOptions(ICreateBrowser):
    defaultViewport: Optional[Any] = None

"""
Pyppeteer specific launch options
"""
@dataclass
class PyppeteerLaunchOptions(BaseLaunchOptions):
    defaultViewport: Optional[Any] = None

"""
Playwright specific launch options
"""
@dataclass
class PlaywrightLaunchOptions(BaseLaunchOptions):
    pass

"""
Captcha detection and solving response
"""
@dataclass
class CaptchaCDPResponse:
    success: bool
    message: str
    type: Optional[str] = None
    token: Optional[str] = None

"""
Captcha configuration options
"""
@dataclass
class CaptchaOptions:
    type: str
    disabled: bool

"""
Auto-solve configuration options
"""
@dataclass
class SetAutoSolveOptions:
    autoSolve: Optional[bool] = None
    options: Optional[List[CaptchaOptions]] = None

@dataclass
class LiveURLResponse:
    error: Optional[str]
    liveURL: Optional[str]

@dataclass
class ImageToTextOptions:
    imageSelector: str
    inputSelector: str
    timeout: Optional[int] = None

@dataclass
class SetConfigOptions:
    apiKey: Optional[str] = None
    autoSolve: Optional[bool] = None
    enabledForRecaptcha: Optional[bool] = None
    enabledForRecaptchaV3: Optional[bool] = None
    enabledForTurnstile: Optional[bool] = None
    enabledForHcaptcha: Optional[bool] = None
    enabledForAws: Optional[bool] = None
    cloudflareMode: Optional[str] = None 