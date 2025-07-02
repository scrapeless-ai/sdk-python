import requests
from typing import Optional, Dict, Any
from ..error import ScrapelessError
from ..utils import Logger

class BaseService:
    def __init__(self, api_key: str, base_url: str, timeout: int = 30000, handle_response=None):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout / 1000
        self.handle_response = handle_response
        self.log = Logger().with_prefix('BaseService')

    def request(
        self,
        endpoint: str,
        method: str = 'GET',
        body: Optional[Dict] = None,
        additional_headers: Optional[Dict[str, str]] = None,
        response_with_status: bool = False
    ):
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': self.api_key
        }
        if additional_headers:
            headers.update(additional_headers)

        url = f"{self.base_url}{endpoint}"
        options = {
            'headers': headers,
            'timeout': self.timeout
        }
        if method.upper() in ['POST', 'PUT', 'DELETE']:
            if body is not None:
                if headers.get('Content-Type', '').startswith('multipart/form-data'):
                    options['files'] = body
                else:
                    options['json'] = body
        elif method.upper() == 'GET' and body is not None:
            options['params'] = body

        try:
            response = requests.request(method, url, **options)
        except Exception as e:
            self.log.error(f"Request failed: {e}")
            raise ScrapelessError(f"Request failed: {e}")

        content_type = response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            data = response.json()
        else:
            data = response.text

        if not response.ok:
            error_message = ''
            if isinstance(data, dict):
                error_message = data.get('error') or data.get('msg') or ''

                if 'traceId' in data:
                    if error_message:
                        error_message += f" (TraceID: {data['traceId']})"
                    else:
                        error_message = f"failed with status {response.status_code} (TraceID: {data['traceId']})"
            if not error_message:
                error_message = f"failed with status {response.status_code}"
            error_message = f"Request {method} {url} {error_message}"
            self.log.error(error_message)
            raise ScrapelessError(error_message)

        if self.handle_response:
            return self.handle_response(data)

        if response_with_status:
            return {'data': data, 'status': response.status_code}
        else:
            return data.get('data', data) 