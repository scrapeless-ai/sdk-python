from dataclasses import asdict
from .base import BaseService
from ..utils.utils import sleep
from ..types.captcha import ICreateCaptcha

"""
Captcha service class for interacting with the Scrapeless Captcha API
"""
class CaptchaService(BaseService):
    base_path = '/api/v1'

    def __init__(self, api_key: str, base_url: str, timeout: int):
        super().__init__(api_key, base_url, timeout)

    def captcha_create(self, data: ICreateCaptcha):
        payload_dict = asdict(data)
        return self.request(f"{self.base_path}/createTask", 'POST', payload_dict, response_with_status=True)

    def captcha_result_get(self, task_id: str):
        return self.request(f"{self.base_path}/getTaskResult/{task_id}", 'GET', response_with_status=True)

    def captcha_solver(self, data: ICreateCaptcha):
        task = self.captcha_create(data)
        result = self.captcha_result_get(task['data']['taskId'])
        if result['data']['success']:
            return result['data']
        while True:
            sleep(1000)
            result = self.captcha_result_get(task['data']['taskId'])
            if result['data']['success']:
                return result['data'] 