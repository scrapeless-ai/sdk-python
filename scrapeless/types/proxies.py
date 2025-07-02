from dataclasses import dataclass

"""
Proxy configuration interface for creating residential proxies
"""
@dataclass
class ICreateProxy:
    country: str
    session_duration: int
    session_id: str
    gateway: str
