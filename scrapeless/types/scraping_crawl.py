from dataclasses import dataclass
from typing import Optional, List, Dict, Any

"""
Configuration interface for ScrapingCrawl
"""
@dataclass
class ScrapingCrawlConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    timeout: Optional[int] = None

@dataclass
class ScrapingCrawlDocumentMetadata:
    title: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = None
    keywords: Optional[str] = None
    robots: Optional[str] = None
    ogTitle: Optional[str] = None
    ogDescription: Optional[str] = None
    ogUrl: Optional[str] = None
    ogImage: Optional[str] = None
    ogAudio: Optional[str] = None
    ogDeterminer: Optional[str] = None
    ogLocale: Optional[str] = None
    ogLocaleAlternate: Optional[List[str]] = None
    ogSiteName: Optional[str] = None
    ogVideo: Optional[str] = None
    dctermsCreated: Optional[str] = None
    dcDateCreated: Optional[str] = None
    dcDate: Optional[str] = None
    dctermsType: Optional[str] = None
    dcType: Optional[str] = None
    dctermsAudience: Optional[str] = None
    dctermsSubject: Optional[str] = None
    dcSubject: Optional[str] = None
    dcDescription: Optional[str] = None
    dctermsKeywords: Optional[str] = None
    modifiedTime: Optional[str] = None
    publishedTime: Optional[str] = None
    articleTag: Optional[str] = None
    articleSection: Optional[str] = None
    sourceURL: Optional[str] = None
    statusCode: Optional[int] = None
    error: Optional[str] = None
    # Additional metadata fields can be added as needed

@dataclass
class ScrapingCrawlDocument:
    markdown: Optional[str] = None
    html: Optional[str] = None
    rawHtml: Optional[str] = None
    links: Optional[List[str]] = None
    extract: Optional[Any] = None
    screenshot: Optional[str] = None
    metadata: Optional[ScrapingCrawlDocumentMetadata] = None

@dataclass
class CrawlScrapeOptions:
    formats: Optional[List[str]] = None
    headers: Optional[Dict[str, str]] = None
    includeTags: Optional[List[str]] = None
    excludeTags: Optional[List[str]] = None
    onlyMainContent: Optional[bool] = None
    waitFor: Optional[int] = None
    timeout: Optional[int] = None

@dataclass
class ScrapeParams(CrawlScrapeOptions):
    browserOptions: Optional[Dict[str, Any]] = None

@dataclass
class ScrapeStatusResponse:
    success: bool
    error: Optional[str]
    status: str
    data: ScrapingCrawlDocument

@dataclass
class CrawlParams:
    includePaths: Optional[List[str]] = None
    excludePaths: Optional[List[str]] = None
    maxDepth: Optional[int] = None
    maxDiscoveryDepth: Optional[int] = None
    limit: Optional[int] = None
    allowBackwardLinks: Optional[bool] = None
    allowExternalLinks: Optional[bool] = None
    ignoreSitemap: Optional[bool] = None
    scrapeOptions: Optional[CrawlScrapeOptions] = None
    deduplicateSimilarURLs: Optional[bool] = None
    ignoreQueryParameters: Optional[bool] = None
    regexOnFullURL: Optional[bool] = None
    delay: Optional[int] = None
    browserOptions: Optional[Dict[str, Any]] = None

@dataclass
class ScrapeResponse:
    id: Optional[str]
    success: bool
    error: Optional[str]

@dataclass
class BatchScrapeResponse:
    id: Optional[str]
    success: bool
    error: Optional[str]
    invalidURLs: Optional[List[str]] = None

@dataclass
class CrawlResponse:
    id: Optional[str]
    success: bool
    error: Optional[str]

@dataclass
class CrawlStatusResponse:
    success: bool
    status: str
    completed: int
    total: int
    data: List[ScrapingCrawlDocument]
    error: Optional[str] = None

@dataclass
class BatchScrapeStatusResponse:
    success: bool
    status: str
    completed: int
    total: int
    data: List[ScrapingCrawlDocument]
    error: Optional[str] = None

@dataclass
class ErrorResponse:
    success: bool
    error: str

@dataclass
class CrawlErrorsResponse:
    errors: List[Dict[str, Any]]
    robotsBlocked: List[str] 