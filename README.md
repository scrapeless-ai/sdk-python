# Scrapeless Python SDK

The official Python SDK for [Scrapeless AI](https://scrapeless.com) - End-to-End Data Infrastructure for AI Developers & Enterprises.

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
- **Universal Scraping API**: web interaction and data extraction with full browser capabilities. Execute JavaScript rendering, simulate user interactions (clicks, scrolls), bypass anti-scraping measures, and export structured data in formats.
- **Crawl**: Extract data from single pages or traverse entire domains, exporting in formats including Markdown, JSON, HTML, screenshots, and links.
- **Scraping API**: Direct data extraction APIs for websites (e.g., e-commerce, travel platforms). Retrieve structured product information, pricing, and reviews with pre-built connectors.
- **Deep SerpApi**: Google SERP data extraction API. Fetch organic results, news, images, and more with customizable parameters and real-time updates.
- **Proxies**: Geo-targeted proxy network with 195+ countries. Optimize requests for better success rates and regional data access.
- **Actor**: Deploy custom crawling and data processing workflows at scale with built-in scheduling and resource management.
- **Storage Solutions**: Scalable data storage solutions for crawled content, supporting seamless integration with cloud services and databases.

## 📦 Installation

Install the SDK using pip:

```bash
pip install scrapeless
```

## 🚀 Quick Start

### Prerequisite

[Log in](https://app.scrapeless.com) to the Scrapeless Dashboard and get the API Key

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
SCRAPELESS_ACTOR_API_URL=https://actor.scrapeless.com
SCRAPELESS_STORAGE_API_URL=https://storage.scrapeless.com
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

### Crawl

Extract data from single pages or traverse entire domains, exporting in formats including Markdown, JSON, HTML, screenshots, and links.

```python
from scrapeless import Scrapeless

client = Scrapeless()

result = client.scraping_crawl.scrape_url("https://example.com")
print(result)
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

### Deep SerpApi

Google SERP data extraction API. Fetch organic results, news, images, and more with customizable parameters and real-time updates:

```python
from scrapeless import Scrapeless
from scrapeless.types import ScrapingTaskRequest

client = Scrapeless()
request = ScrapingTaskRequest(
    actor='scraper.google.search',
    input={'q': 'nike site:www.nike.com'}
)
result = client.deepserp.scrape(request=request)
print(result)
```

### Actor

Deploy custom crawling and data processing workflows at scale with built-in scheduling and resource management:

```python
from scrapeless import Scrapeless
from scrapeless.types import IRunActorData, IActorRunOptions

client = Scrapeless()
data = IRunActorData(
    input={'url': 'https://example.com'},
    run_options=IActorRunOptions(
        CPU=2,
        memory=2048,
        timeout=600,
    )
)

run = client.actor.run(
    actor_id='your_actor_id',
    data=data
)
print('Actor run result:', run)
```

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

## 🔧 API Reference

### Client Configuration

```python
from scrapeless.types import ScrapelessConfig 

config = ScrapelessConfig(
    api_key='', # Your api key
    timeout=30000, # Request timeout in milliseconds (default: 30000)
    base_api_url='', # Base API URL
    actor_api_url='', # Actor service URL
    storage_api_url='', # Storage service URL
    browser_api_url='', # Browser service URL
    scraping_crawl_api_url='' # Crawl service URL
)
```

### Available Services

The SDK provides the following services through the main client:

- `client.browser` - browser automation with Playwright/Pyppeteer support, anti-detection tools (fingerprinting, CAPTCHA solving), and extensible workflows.
- `client.universal` - JS rendering, user simulation (clicks/scrolls), anti-block bypass, and structured data export.
- `client.scraping_crawl` - Recursive site crawling with multi-format export (Markdown, JSON, HTML, screenshots, links).
- `client.scraping` - Pre-built connectors for sites (e.g., e-commerce, travel) to extract product data, pricing, and reviews.
- `client.deepserp` - Search engine results extraction
- `client.proxies` - Proxy management
- `client.actor` - Scalable workflow automation with built-in scheduling and resource management.
- `client.storage` - Data storage solutions

## 📚 Examples

Check out the [`examples`](./examples) directory for comprehensive usage examples:

- [Browser](./examples/browser_example.py)
- [Playwright Integration](./examples/playwright_example.py)
- [Pyppeteer Integration](./examples/pyppeteer_example.py)
- [Scraping API](./examples/scraping_example.py)
- [Actor](./examples/actor_example.py)
- [Storage Usage](./examples/storage_example.py)
- [Proxies](./examples/proxies_example.py)
- [Deep SerpApi](./examples/deepserp_example.py)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- 📖 **Documentation**: [https://docs.scrapeless.com](https://docs.scrapeless.com)
- 💬 **Community**: [Join our Discord](https://backend.scrapeless.com/app/api/v1/public/links/discord)
- 🐛 **Issues**: [GitHub Issues](https://github.com/scrapeless-ai/sdk-python/issues)
- 📧 **Email**: [support@scrapeless.com](mailto:support@scrapeless.com)

## 🏢 About Scrapeless

Scrapeless is a powerful web scraping and browser automation platform that helps businesses extract data from any website at scale. Our platform provides:

- High-performance web scraping infrastructure
- Global proxy network
- Browser automation capabilities
- Enterprise-grade reliability and support

Visit [scrapeless.com](https://scrapeless.com) to learn more and get started.

---

Made with ❤️ by the Scrapeless team
