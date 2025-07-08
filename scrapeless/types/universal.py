from dataclasses import dataclass
from typing import Optional, List, Dict, Any, TypeVar, Generic

T = TypeVar('T')
R = TypeVar('R')

"""
Universal Scraping API Request Parameters
"""
@dataclass
class UniversalScrapingRequest(Generic[T, R]):
    actor: str
    input: T
    proxy: Optional[R] = None

@dataclass
class UniversalProxy:
    country: str

@dataclass
class UniversalJsRenderInput:
    url: str
    headless: Optional[bool] = None
    js_render: Optional[bool] = None
    js_instructions: Optional[List[Dict[str, Any]]] = None
    block: Optional[Dict[str, List[str]]] = None

@dataclass
class JsInstruction:
    click: Optional[List[Any]] = None
    evaluate: Optional[str] = None
    fill: Optional[List[str]] = None
    keyboard: Optional[List[Any]] = None
    wait: Optional[int] = None
    wait_for: Optional[List[Any]] = None
    # Additional properties can be added as needed

@dataclass
class UniversalWebUnlockerInput:
    url: str
    type: str
    redirect: bool
    method: str
    request_id: Optional[str] = None
    extractor: Optional[str] = None
    header: Optional[Dict[str, str]] = None

@dataclass
class UniversalAkamaiWebCookieInput:
    type: str
    url: str
    user_agent: str

@dataclass
class UniversalAkamaiWebSensorInput:
    abck: str
    bmsz: str
    url: str
    userAgent: str

@dataclass
class UniversalConfig:
    api_key: Optional[str] = None
    timeout: Optional[int] = None 