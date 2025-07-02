from .base import BaseService
from ..types.proxies import ICreateProxy
import time
import random

"""
ProxiesService provides functionality for working with residential proxies
"""
class ProxiesService(BaseService):
    def __init__(self, api_key: str, base_url: str, timeout: int):
        super().__init__(api_key, base_url, timeout)

    def proxy(self, proxy: ICreateProxy) -> str:
        token = self.api_key
        base_url = 'http://CHANNEL-proxy.residential-country_'
        return f"{base_url}{proxy.country}-r_{proxy.session_duration}m-s_{proxy.session_id}:{token}@{proxy.gateway}"

    def create_proxy(self, options: ICreateProxy) -> str:
        return self.proxy(options)

    def generate_session_id(self) -> str:
        timestamp = format(int(time.time()), 'x')
        random_str = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
        return f"{timestamp}-{random_str}" 