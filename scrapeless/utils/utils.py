import time
import random
import string
from urllib.parse import urlparse, parse_qs
from datetime import datetime

"""
Base utility functions collection
"""

def sleep(ms: int):
    """
    Sleep for specified milliseconds
    """
    time.sleep(ms / 1000)

def retry(fn, max_attempts=3, delay=1000, backoff=True, on_retry=None):
    """
    Retry a specified function until success or maximum attempts reached
    """
    attempt = 0
    last_error = Exception('Retry failed')
    while attempt < max_attempts:
        try:
            return fn()
        except Exception as error:
            last_error = error
            attempt += 1
            if attempt >= max_attempts:
                break
            if on_retry:
                on_retry(attempt, last_error)
            wait_time = delay * (2 ** (attempt - 1)) if backoff else delay
            sleep(wait_time)
    raise last_error

def parse_url(url: str):
    """
    Parse URL, extract domain and path
    """
    try:
        parsed = urlparse(url)
        query = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(parsed.query).items()}
        return {
            'protocol': parsed.scheme,
            'hostname': parsed.hostname,
            'path': parsed.path,
            'query': query,
            'fragment': parsed.fragment
        }
    except Exception:
        raise ValueError(f"Invalid URL: {url}")

def random_string(length=10):
    """
    Generate random string
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def is_browser():
    """
    Detect browser environment (always False in Python)
    """
    return False

def format_date(date, format_str='YYYY-MM-DD HH:mm:ss'):
    """
    Format date
    """
    if isinstance(date, (int, float)):
        d = datetime.fromtimestamp(date)
    elif isinstance(date, str):
        d = datetime.fromisoformat(date)
    else:
        d = date
    replacements = {
        'YYYY': d.strftime('%Y'),
        'MM': d.strftime('%m'),
        'DD': d.strftime('%d'),
        'HH': d.strftime('%H'),
        'mm': d.strftime('%M'),
        'ss': d.strftime('%S'),
    }
    for k, v in replacements.items():
        format_str = format_str.replace(k, v)
    return format_str 