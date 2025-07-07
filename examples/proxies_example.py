"""
Scrapeless Python SDK - Proxies Service Example
This example demonstrates how to use the ProxiesService to generate and work
with residential proxies.
"""
import os
from scrapeless import Scrapeless
from scrapeless.types import ICreateProxy

def test_create_proxy() -> str:
    """
    Test creating a proxy with specific parameters
    """
    try:
        print('Testing proxy creation with specific parameters...')
        proxy = ICreateProxy(
            country='US',
            session_duration=30,
            session_id='test-session-123',
            gateway='gate.smartproxy.com:7000'
        )
        proxy_url = client.proxies.proxy(proxy)
        print('✅ Proxy URL generated successfully')
        print('Proxy URL:', proxy_url)
        return proxy_url
    except Exception as error:
        print(f'❌ Proxy creation failed: {error}')
        raise

def test_create_proxy_alias() -> str:
    """
    Test creating a proxy with the create_proxy method
    """
    try:
        print('Testing create_proxy alias method...')
        proxy = ICreateProxy(
            country='UK',
            session_duration=60,
            session_id='test-session-456',
            gateway='gate.smartproxy.com:7000'
        )
        proxy_url = client.proxies.create_proxy(proxy)
        print('✅ Proxy URL generated successfully using create_proxy')
        print('Proxy URL:', proxy_url)
        return proxy_url
    except Exception as error:
        print(f'❌ create_proxy method failed: {error}')
        raise

def test_generate_session_id() -> dict:
    """
    Test generating a session ID
    """
    try:
        print('Testing session ID generation...')
        session_id = client.proxies.generate_session_id()
        print('✅ Session ID generated successfully')
        print('Session ID:', session_id)
        # Create a proxy with the generated session ID
        proxy = ICreateProxy(
            country='JP',
            session_duration=15,
            session_id=session_id,
            gateway='gate.smartproxy.com:7000'
        )
        proxy_url = client.proxies.proxy(proxy)
        print('Created proxy with generated session ID:', proxy_url)
        return {'session_id': session_id, 'proxy_url': proxy_url}
    except Exception as error:
        print(f'❌ Session ID generation failed: {error}')
        raise

def run_example() -> None:
    """
    Main entry for running all proxies service tests.
    """
    print('=== Scrapeless Proxies Service Tests ===\n')
    try:
        # Test proxy creation
        test_create_proxy()
        print('\n')
        # Test create_proxy alias
        test_create_proxy_alias()
        print('\n')
        # Test session ID generation
        test_generate_session_id()
        print('\n')
        print('🎉 All tests completed successfully')
    except Exception as error:
        print(f'❌ Tests failed with error: {error}')

# Initialize the client
def _init_client() -> Scrapeless:
    api_key = os.getenv('SCRAPELESS_API_KEY') or 'your_api_key_here'
    return Scrapeless({
        'api_key': api_key,
    })

global client
client = _init_client()

run_example() 