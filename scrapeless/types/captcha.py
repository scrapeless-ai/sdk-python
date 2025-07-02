from dataclasses import dataclass
from typing import Optional, Callable, Any

"""
Legacy SDK compatibility type: Captcha request
"""
@dataclass
class ICreateCaptcha:
    actor: str
    input: dict
    proxy: Optional[str] = None

"""
Legacy SDK compatibility type: Captcha response
"""
@dataclass
class ICreateCaptchaResponse:
    state: str  # 'idle'
    success: bool
    taskId: str

"""
Legacy SDK compatibility type: Captcha result
"""
@dataclass
class IGetCaptchaResult:
    actor: str
    createTime: int
    elapsed: int
    state: Optional[str]
    solution: dict
    success: bool
    taskId: str