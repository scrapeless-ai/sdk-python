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

- **Browser**: Advanced browser session management supporting Playwright and Puppeteer frameworks, with configurable anti-detection capabilities (e.g., fingerprint spoofing, CAPTCHA solving) and extensible automation workflows.
- **Universal Scraping API**: web interaction and data extraction with full browser capabilities. Execute JavaScript rendering, simulate user interactions (clicks, scrolls), bypass anti-scraping measures, and export structured data in formats.
- **Crawl**: Extract data from single pages or traverse entire domains, exporting in formats including Markdown, JSON, HTML, screenshots, and links.
- **Scraping API**: Direct data extraction APIs for websites (e.g., e-commerce, travel platforms). Retrieve structured product information, pricing, and reviews with pre-built connectors.
- **Deep SerpApi**: Google SERP data extraction API. Fetch organic results, news, images, and more with customizable parameters and real-time updates.
- **Proxies**: Geo-targeted proxy network with 195+ countries. Optimize requests for better success rates and regional data access.
- **Actor**: Deploy custom crawling and data processing workflows at scale with built-in scheduling and resource management.
- **Storage Solutions**: Scalable data storage solutions for crawled content, supporting seamless integration with cloud services and databases.
- **TypeScript Support**: Full TypeScript definitions for better development experience

## 📦 Installation

Install the SDK using pip:

```bash
pip install @scrapeless-ai/sdk
```

## 🚀 Quick Start

### Prerequisite

[Log in](https://app.dashboard.scrapeless.com) to the Scrapeless Dashboard and get the API Key

### Basic Setup

```python
from scrapeless import ScrapelessClient

client = ScrapelessClient({
  'api_key': 'your-api-key' # Get your API key from https://scrapeless.com
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

Advanced browser session management supporting Playwright and Puppeteer frameworks, with configurable anti-detection capabilities (e.g., fingerprint spoofing, CAPTCHA solving) and extensible automation workflows:

```python
from scrapeless import ScrapelessClient
from scrapeless.types import ICreateBrowser
import pyppeteer

client = ScrapelessClient()

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
    browser = await pyppeteer.connect({ 'browserWSEndpoint': browser_ws_endpoint })
    # Open new page and navigate to website
    page = await browser.newPage()
    await page.goto('https://www.scrapeless.com')
```

### Crawl

单页或全站爬取，支持多种格式导出（Markdown、JSON、HTML、截图、链接等）。

```python
from scrapeless import ScrapelessClient

client = ScrapelessClient()

# 爬取单个页面
result = client.scraping_crawl.scrape_url("https://example.com")
print(result)
```

### Scraping API

直接数据提取 API，适用于电商、旅游等网站，获取结构化商品信息、价格和评论：

```python
from scrapeless import ScrapelessClient
from scrapeless.types import ScrapingTaskRequest

client = ScrapelessClient()
request = ScrapingTaskRequest(
    actor='scraper.google.search',
    input={'q': 'nike site:www.nike.com'}
)
result = client.scraping.scrape(request=request)
print(result['data'])
```

### Deep SerpApi

Google SERP 数据提取 API，支持自定义参数和实时更新：

```python
from scrapeless import ScrapelessClient
from scrapeless.types import ScrapingTaskRequest

client = ScrapelessClient()
request = ScrapingTaskRequest(
    actor='scraper.google.search',
    input={'q': 'nike site:www.nike.com'}
)
results = client.deepserp.scrape(request=request)
print(results)
```

### Actor

大规模自定义爬取和数据处理工作流，支持调度和资源管理：

```python
from scrapeless import ScrapelessClient
from scrapeless.types import IRunActorData, IActorRunOptions

client = ScrapelessClient()
data = IRunActorData(
    input={ 'url': 'https://example.com' },
    run_options=IActorRunOptions(
        CPU=2,
        memory=2048,
        timeout=600,
    )
)

# 运行一个actor
run = client.actor.run(
    actor_id='your_actor_id',
    data=data
)
print('Actor运行结果:', run)
```

### 错误处理

SDK 会抛出 `ScrapelessError` 处理 API 相关错误：

```python
from scrapeless import ScrapelessClient, ScrapelessError

client = ScrapelessClient()
try:
    result = client.scraping.scrape({ 'url': 'invalid-url' })
except ScrapelessError as error:
    print(f"Scrapeless API 错误: {error}")
    if hasattr(error, 'status_code'):
        print(f"状态码: {error.status_code}")
```

## 🔧 API Reference

### Client Configuration

```typescript
interface ScrapelessConfig {
  apiKey?: string; // Your API key
  timeout?: number; // Request timeout in milliseconds (default: 30000)
  baseApiUrl?: string; // Base API URL
  actorApiUrl?: string; // Actor service URL
  storageApiUrl?: string; // Storage service URL
  browserApiUrl?: string; // Browser service URL
  scrapingCrawlApiUrl?: string; // Crawl service URL
}
```

### Available Services

The SDK provides the following services through the main client:

- `client.browser` - browser automation with Playwright/Puppeteer support, anti-detection tools (fingerprinting, CAPTCHA solving), and extensible workflows.
- `client.universal` - JS rendering, user simulation (clicks/scrolls), anti-block bypass, and structured data export.
- `client.scrapingCrawl` - Recursive site crawling with multi-format export (Markdown, JSON, HTML, screenshots, links).
- `client.scraping` - Pre-built connectors for sites (e.g., e-commerce, travel) to extract product data, pricing, and reviews.
- `client.deepserp` - Search engine results extraction
- `client.proxies` - Proxy management
- `client.actor` - Scalable workflow automation with built-in scheduling and resource management.
- `client.storage` - Data storage solutions

### Error Handling

The SDK throws `ScrapelessError` for API-related errors:

```javascript
import { ScrapelessError } from "@scrapeless-ai/sdk";

try {
  const result = await client.scraping.scrape({ url: "invalid-url" });
} catch (error) {
  if (error instanceof ScrapelessError) {
    console.error(`Scrapeless API Error: ${error.message}`);
    console.error(`Status Code: ${error.statusCode}`);
  }
}
```

## 📚 Examples

Check out the [`examples`](./examples) directory for comprehensive usage examples:

- [Browser](./examples/browser_example.py)
- [Playwright Integration](./examples/playwright_example.py)
- [Puppeteer Integration](./examples/puppeteer_example.py)
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
- 🐛 **Issues**: [GitHub Issues](https://github.com/scrapeless-ai/sdk-node/issues)
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
