from dataclasses import dataclass
from typing import Optional, List, Dict, Any

"""
SERP API Request Parameters
"""
@dataclass
class SerpRequest:
    query: str
    country: Optional[str] = None
    language: Optional[str] = None
    device: Optional[str] = None  # 'desktop' | 'mobile' | 'tablet'
    page: Optional[int] = None
    pageSize: Optional[int] = None
    params: Optional[Dict[str, str]] = None
    engine: Optional[str] = None  # 'google' | 'bing' | 'yahoo' | 'yandex' | 'duckduckgo'
    proxy: Optional[Any] = None

@dataclass
class SerpOrganicResult:
    position: int
    title: str
    url: str
    displayUrl: str
    snippet: str
    cachedUrl: Optional[str] = None
    relatedUrl: Optional[str] = None
    sitelinks: Optional[List[Dict[str, Any]]] = None

@dataclass
class SerpAdResult:
    position: int
    title: str
    url: str
    displayUrl: str
    snippet: str
    sitelinks: Optional[List[Dict[str, Any]]] = None

@dataclass
class SerpLocalResult:
    position: int
    title: str
    address: str
    website: Optional[str] = None
    phone: Optional[str] = None
    rating: Optional[float] = None
    reviewCount: Optional[int] = None
    categories: Optional[List[str]] = None
    hours: Optional[Dict[str, str]] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

@dataclass
class SerpProductResult:
    position: int
    title: str
    url: str
    price: Optional[str] = None
    currency: Optional[str] = None
    merchant: Optional[str] = None
    imageUrl: Optional[str] = None
    rating: Optional[float] = None
    reviewCount: Optional[int] = None

@dataclass
class SerpResult:
    status: str  # 'success' | 'error'
    query: str
    engine: str
    totalResults: Optional[int] = None
    searchTime: Optional[float] = None
    organic: Optional[List[SerpOrganicResult]] = None
    ads: Optional[List[SerpAdResult]] = None
    local: Optional[List[SerpLocalResult]] = None
    products: Optional[List[SerpProductResult]] = None
    knowledgeGraph: Optional[Dict[str, Any]] = None
    relatedSearches: Optional[List[str]] = None
    error: Optional[str] = None
    requestId: str = ''
    timestamp: str = '' 