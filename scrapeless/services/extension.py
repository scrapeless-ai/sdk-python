import os
from .base import BaseService
from ..types.extension import UploadExtensionResponse, ExtensionDetail, ExtensionListItem
from typing import Optional

"""
Extension service class for browser extension management
"""
class ExtensionService(BaseService):
    def __init__(self, api_key: str, base_url: str, timeout: int):
        super().__init__(api_key, base_url, timeout)

    def _get_file_name(self, file_path: str) -> str:
        valid_suffixes = ['.zip']
        file_suffix = os.path.splitext(file_path)[1].lower()
        if file_suffix not in valid_suffixes:
            raise ValueError(f"Invalid file suffix: {file_suffix}. Supported suffixes: {', '.join(valid_suffixes)}")
        return os.path.basename(file_path)

    def upload(self, file_path: str, name: str) -> UploadExtensionResponse:
        file_name = self._get_file_name(file_path)
        with open(file_path, 'rb') as file_stream:
            files = {
                'file': (file_name, file_stream, 'application/zip'),
                'name': (None, name)
            }
            res = self.request('/browser/extensions/upload', 'POST', files, {'Content-Type': 'multipart/form-data'}, True)
        return UploadExtensionResponse(**res['data'])
    def update(self, extension_id: str, file_path: str, name: Optional[str] = None) -> dict:
        file_name = self._get_file_name(file_path)
        with open(file_path, 'rb') as file_stream:
            files = {
                'file': (file_name, file_stream, 'application/zip')
            }
            if name:
                files['name'] = name
            res = self.request(f'/browser/extensions/{extension_id}', 'PUT', files, {'Content-Type': 'multipart/form-data'}, True)
        return res['data']

    def get(self, extension_id: str) -> ExtensionDetail:
        res = self.request(f'/browser/extensions/{extension_id}', 'GET', response_with_status=True)
        return ExtensionDetail(**res['data'])

    def list(self) -> list:
        res = self.request('/browser/extensions/list', 'GET', response_with_status=True)
        return [ExtensionListItem(**item) for item in res['data']]

    def delete(self, extension_id: str) -> dict:
        res = self.request(f'/browser/extensions/{extension_id}', 'DELETE', response_with_status=True)
        return res['data'] 