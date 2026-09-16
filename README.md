# Scrapeless Python SDK

The official Python SDK for [Scrapeless AI](https://scrapeless.com?utm_source=github&utm_medium=referral&utm_campaign=python_sdk_repo) - End-to-End Data Infrastructure for AI Developers & Enterprises.

New to Scrapeless? [Sign up](https://app.scrapeless.com/passport/login?utm_source=github&utm_medium=referral&utm_campaign=python_sdk_repo) and get $5 in free credits.

## 📑 Table of Contents

- [🌟 Features](#-features)
- [📦 Installation](#-installation)
- [🚀 Quick Start](#-quick-start)
- [📖 Usage Examples](#-usage-examples)
- [🔧 API Reference](#-api-reference)
- [📚 Examples](#-examples)
- [📄 License](#-license)
- [📞 Support](#-support)
- [🏢 About Scrapeless](#-about-scrapeless)

## 🌟 Features

- **Browser**: Advanced browser session management supporting Playwright and pyppeteer frameworks, with configurable anti-detection capabilities (e.g., fingerprint spoofing, CAPTCHA solving) and extensible automation workflows.
- **Web Unlocker**: web interaction and data extraction with full browser capabilities. Execute JavaScript rendering, simulate user interactions (clicks, scrolls), bypass anti-scraping measures, and export structured data in formats.
- **Crawl**: Extract data from single pages or traverse entire domains, exporting in formats including Markdown, JSON, HTML, screenshots, and links.
- **Scraping API**: Direct data extraction APIs for websites (e.g., e-commerce, travel platforms). Retrieve structured product information, pricing, and reviews with pre-built connectors.
- **Google Search API**: Google SERP data extraction API. Fetch organic results, news, images, and more with customizable parameters and real-time updates.
- **AI Scraper**: Extract AI chat answers, citations, and brand mentions across supported models.
- **Proxies**: Geo-targeted proxy network with 195+ countries. Optimize requests for better success rates and regional data access.

## 📦 Installation

Install the SDK using pip:

```bash
pip install scrapeless
```

## 🚀 Quick Start

### Prerequisite

[Log in](https://app.scrapeless.com?utm_source=github&utm_medium=referral&utm_campaign=python_sdk_repo) to the Scrapeless Dashboard and get the API Key

### Basic Setup

```python
from scrapeless import Scrapeless

client = Scrapeless({
    'api_key': 'your-api-key'  # Get your API key from https://scrapeless.com
})
```

### Environment Variables

You can also configure the SDK using environment variables:

```bash
# Required
SCRAPELESS_API_KEY=your-api-key

# Optional - Custom API endpoints
SCRAPELESS_BASE_API_URL=https://api.scrapeless.com
SCRAPELESS_BROWSER_API_URL=https://browser.scrapeless.com
SCRAPELESS_CRAWL_API_URL=https://api.scrapeless.com
```

## 📖 Usage Examples

### Browser

Advanced browser session management supporting Playwright and Pyppeteer frameworks, with configurable anti-detection capabilities (e.g., fingerprint spoofing, CAPTCHA solving) and extensible automation workflows:

```python
from scrapeless import Scrapeless
from scrapeless.types import ICreateBrowser
import pyppeteer

client = Scrapeless()


async def example():
    # Create a browser session
    config = ICreateBrowser(
        session_name='sdk_test',
        session_ttl=180,
        proxy_country='US',
        session_recording=True
    )
    session = client.browser.create(config).__dict__
    browser_ws_endpoint = session['browser_ws_endpoint']
    print('Browser WebSocket endpoint created:', browser_ws_endpoint)

    # Connect to browser using pyppeteer
    browser = await pyppeteer.connect({'browserWSEndpoint': browser_ws_endpoint})
    # Open new page and navigate to website
    page = await browser.newPage()
    await page.goto('https://www.scrapeless.com')
```

### Browser Profile

Manage browser profiles for persistent sessions.

```python
from scrapeless import Scrapeless

client = Scrapeless()
profile = client.profiles.create('My Profile')
print(profile)
```

### Scraping API

Direct data extraction APIs for websites (e.g., e-commerce, travel platforms). Retrieve structured product information, pricing, and reviews with pre-built connectors:

```python
from scrapeless import Scrapeless
from scrapeless.types import ScrapingTaskRequest

client = Scrapeless()
request = ScrapingTaskRequest(
    actor='scraper.google.search',
    input={'q': 'nike site:www.nike.com'}
)
result = client.scraping.scrape(request=request)
print(result)
```

### Web Unlocker

Extract data from websites using Web Unlocker (exposed as `client.universal`).

```python
from scrapeless import Scrapeless
from scrapeless.types import UniversalScrapingRequest

client = Scrapeless()
result = client.universal.scrape(UniversalScrapingRequest(
    actor='unlocker.webunlocker',
    input={'url': 'https://example.com', 'method': 'GET', 'redirect': False}
))
print(result)
```

### Crawl

Extract data from single pages or traverse entire domains, exporting in formats including Markdown, JSON, HTML, screenshots, and links.

```python
from scrapeless import Scrapeless

client = Scrapeless()

result = client.scraping_crawl.scrape_url("https://example.com")
print(result)
```

### Proxy

Generate a proxy URL using your gateway and session settings.

```python
from scrapeless import Scrapeless
from scrapeless.types import ICreateProxy

client = Scrapeless()
proxy_url = client.proxies.proxy(ICreateProxy(
    country='US',
    session_duration=30,
    session_id=client.proxies.generate_session_id(),
    gateway='your-proxy-gateway:port'
))
print(proxy_url)
```

### AI Scraper

Extract AI chat content in bulk to monitor brand mentions, compare answers, and analyze competitive intelligence from the latest models. Retrieve URLs, prompts, Markdown answers, citations, and more through one integration.

Supported actors include `scraper.chatgpt`, `scraper.perplexity`, `scraper.copilot`, `scraper.gemini`, `scraper.aimode`, `scraper.overview`, `scraper.grok`, and `scraper.alexa`. The `input` JSON depends on the actor; see the [AI Scraper documentation](https://docs.scrapeless.com/en/llm-chat-scraper/quickstart/introduction/?utm_source=github&utm_medium=referral&utm_campaign=python_sdk_repo) for detailed parameters. The optional `webhook` JSON contains a callback `url`.

```python
from scrapeless import Scrapeless
from scrapeless.types import AIScraperTaskRequest


def main():
    client = Scrapeless()  # Uses SCRAPELESS_API_KEY
    task = client.ai_scraper.create_task(AIScraperTaskRequest(
        actor='scraper.chatgpt',
        input={
            'prompt': 'Most reliable proxy service for data extraction',
            'country': 'US',
            'web_search': True,
        },
        # Optional: webhook={'url': 'https://your-webhook.example.com'},
    ))
    print('Created task:', task)

    result = client.ai_scraper.get_task_result(task['task_id'])
    print('Task status and result:', result)
    # If status is 'running', call get_task_result again later.
    # If status is 'failed', message contains the failure reason.


if __name__ == '__main__':
    main()
```

Both methods return the API JSON unchanged. Creation returns `task_id`, `status`, and, when available, `task_result`. Result retrieval returns `status`, `task_result` when available, and `message` on failure. Status is `success`, `failed`, or `running`; the SDK does not poll automatically.

`create_task` accepts an `AIScraperTaskRequest` or a dictionary; dictionaries also allow additional API parameters. Responses are dictionaries.

## 🔧 API Reference

### Client Configuration

```python
from scrapeless.types import ScrapelessConfig 

config = ScrapelessConfig(
    api_key='', # Your api key
    timeout=30000, # Request timeout in milliseconds (default: 30000)
    base_api_url='', # Base API URL
    browser_api_url='', # Browser service URL
    scraping_crawl_api_url='' # Crawl service URL
)
```

### Available Services

The SDK provides the following services through the main client:

- `client.browser` - browser automation with Playwright/Pyppeteer support, anti-detection tools (fingerprinting, CAPTCHA solving), and extensible workflows.
- `client.universal` - the Web Unlocker feature: JS rendering, user simulation (clicks/scrolls), anti-block bypass, and structured data export.
- `client.scraping_crawl` - Recursive site crawling with multi-format export (Markdown, JSON, HTML, screenshots, links).
- `client.scraping` - Pre-built connectors for sites (e.g., e-commerce, travel) to extract product data, pricing, and reviews.
- `client.deepserp` - the Google Search API feature: search engine (Google SERP) results extraction
- `client.proxies` - Proxy management
- `client.profiles` - Browser profile management
- `client.ai_scraper` - AI chat task creation and result retrieval

### Error Handling

The SDK throws `ScrapelessError` for API-related errors:

```python
from scrapeless import Scrapeless, ScrapelessError

client = Scrapeless()
try:
    result = client.scraping.scrape({'url': 'invalid-url'})
except ScrapelessError as error:
    print(f"Scrapeless API error: {error}")
    if hasattr(error, 'status_code'):
        print(f"Status code: {error.status_code}")
```

## 📚 Examples

Check out the [`examples`](./examples) directory for comprehensive usage examples:

- [Browser](./examples/browser_example.py)
- [Playwright Integration](./examples/playwright_example.py)
- [Pyppeteer Integration](./examples/pyppeteer_example.py)
- [Browser Profile](./examples/profile_example.py)
- [Scraping API](./examples/scraping_example.py)
- [Web Unlocker](./examples/universal_example.py)
- [Crawl](./examples/scraping_crawl_example.py)
- [AI Scraper](./examples/ai_scraper_example.py)
- [Proxies](./examples/proxies_example.py)
- [Google Search API](./examples/deepserp_example.py)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- 📖 **Documentation**: [https://docs.scrapeless.com](https://docs.scrapeless.com?utm_source=github&utm_medium=referral&utm_campaign=python_sdk_repo)
- 💬 **Community**: [Join our Discord](https://backend.scrapeless.com/app/api/v1/public/links/discord)
- 🐛 **Issues**: [GitHub Issues](https://github.com/scrapeless-ai/sdk-python/issues)
- 📧 **Email**: [support@scrapeless.com](mailto:support@scrapeless.com)

## 🏢 About Scrapeless

Scrapeless is a powerful web scraping and browser automation platform that helps businesses extract data from any website at scale. Our platform provides:

- High-performance web scraping infrastructure
- Global proxy network
- Browser automation capabilities
- Enterprise-grade reliability and support

Visit [scrapeless.com](https://scrapeless.com?utm_source=github&utm_medium=referral&utm_campaign=python_sdk_repo) to learn more and get started.

---

Made with ❤️ by the Scrapeless team

## Related Projects

- [Scrapeless Python SDK](https://github.com/scrapeless-ai/sdk-python)
- [Scrapeless Node.js SDK](https://github.com/scrapeless-ai/sdk-node)
- [Scrapeless Go SDK](https://github.com/scrapeless-ai/sdk-go)
