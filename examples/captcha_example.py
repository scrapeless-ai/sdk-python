"""
Scrapeless Python SDK - Captcha Service Example
"""
import json
import asyncio
from scrapeless import Scrapeless
from scrapeless.types import ICreateCaptcha

# Initialize client
client = Scrapeless()

def recaptcha_example() -> None:
    """
    Example for solving reCAPTCHA
    """
    try:
        print('Testing reCAPTCHA solving...')
        req = ICreateCaptcha(
            actor='captcha.recaptcha',
            input={
                'version': 'v2',
                'pageURL': 'https://www.google.com',
                'siteKey': '6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-',
                'pageAction': 'scraping',
                'invisible': False
            }
        )
        # The SDK may require async, but for demo, use run_until_complete
        result = asyncio.get_event_loop().run_until_complete(client.captcha.captcha_solver(req))
        print('✅ reCAPTCHA solving successful')
        print('Result:', json.dumps(result, indent=2))
    except Exception as error:
        print(f'❌ reCAPTCHA solving failed: {error}')

def hcaptcha_example() -> None:
    """
    Example for solving hCaptcha
    """
    try:
        print('Testing hCaptcha solving...')
        req = ICreateCaptcha(
            actor='captcha.hcaptcha',
            input={
                'sitekey': '10000000-ffff-ffff-ffff-000000000001',
                'url': 'https://hcaptcha.com/playground'
            }
        )
        result = asyncio.get_event_loop().run_until_complete(client.captcha.captcha_solver(req.__dict__))
        print('✅ hCaptcha solving successful')
        print('Result:', json.dumps(result, indent=2))
    except Exception as error:
        print(f'❌ hCaptcha solving failed: {error}')

def captcha_task_status_example() -> None:
    """
    Example for captcha task creation and status checking
    """
    try:
        print('Testing captcha task creation...')
        req = ICreateCaptcha(
            actor='captcha.hcaptcha',
            input={
                'sitekey': '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI',
                'url': 'https://recaptcha-demo.appspot.com'
            }
        )
        task = asyncio.get_event_loop().run_until_complete(client.captcha.captcha_create(req.__dict__))
        print(f"✅ Task creation successful: {task['data']['taskId']}")
        print('Waiting 5 seconds before checking status...')
        asyncio.get_event_loop().run_until_complete(asyncio.sleep(5))
        print('Testing captcha task status check...')
        status = asyncio.get_event_loop().run_until_complete(client.captcha.captcha_result_get(task['data']['taskId']))
        print('✅ Task status check successful')
        print('Status:', json.dumps(status['data'], indent=2))
    except Exception as error:
        print(f'❌ Task creation or status check failed: {error}')

def run_example() -> None:
    """
    Main entry, run all captcha examples in sequence
    """
    try:
        recaptcha_example()
        print('\n')
        hcaptcha_example()
        print('\n')
        captcha_task_status_example()
        print('\n')
        print('🎉 All captcha examples completed')
    except Exception as error:
        print(f'❌ Error occurred during captcha examples: {error}')

run_example() 