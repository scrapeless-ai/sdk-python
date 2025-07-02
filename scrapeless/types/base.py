from typing import Generic, TypeVar, Dict

T = TypeVar('T')

"""
Response structure for API requests with status
"""
class ResponseWithStatus(Generic[T]):
    def __init__(self, status: int, data: T):
        self.status = status
        self.data = data

# Type alias for request/response
RequestResponse = Dict[str, object]