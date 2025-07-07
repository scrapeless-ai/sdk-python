"""
Example: Demonstrating how to use the log module with prefixes
Filename: logger_prefix_example.py
"""
from scrapeless import Logger

def logger_prefix_example() -> None:
    """
    Main function to demonstrate logger prefix usage.
    """
    try:
        # Example 1: Using static prefix for all logs
        log = Logger()
        log.with_prefix('Scrapeless')
        log.info('Detecting rendering type for https://www.scrapeless.io/')
        log.debug('Using detection strategy: userAgent')
        log.warn('Connection is slow, timeout increased to 30s')

        # Example 2: Create different loggers with different prefixes
        browser_log = log.with_prefix('Browser')
        proxy_log = log.with_prefix('ProxyManager')

        browser_log.info('Starting new browser session')
        proxy_log.info('Selecting proxy from pool')
        log.info('This log still uses Scrapeless prefix')

        # Example 4: Format logs with placeholders (using f-strings in Python)
        url = 'https://example.com'
        time_ms = 1250
        browser_log.info(f'Navigation to {url} completed in {time_ms}ms')

        # Example 5: Multiple parameters (logging a dictionary)
        stats = {
            'latency': '120ms',
            'country': 'US',
            'alive': True
        }
        proxy_log.debug(f'Connection stats: {stats}')

        print('\nLogger prefix example completed. Check the logs above to see prefixes with colors.')
    except Exception as error:
        print('Logger prefix example error:', error)

def run_example() -> None:
    """
    Main entry for running the logger prefix example.
    """
    logger_prefix_example()
    print('Logger prefix example finished.')

run_example() 