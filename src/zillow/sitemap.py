"""
Module for collecting listings from Zillow Sitemap
"""

import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from prefect import task
from prefect.tasks import exponential_backoff

from zillow.mongo_models.sitemap_model import Property, PropertySet


@task(name="Collects Sitemap partitions")
def collect_sitemap_indexes(html_bytes: bytes) -> list:
    """
    Parses HTML and converts partitions into a list

    Args:
        html_bytes: Incoming sitemap directory html bytes

    Returns:
        sitemaps: list of sitemap urls

    """
    soup = BeautifulSoup(html_bytes, "html.parser")

    sitemaps = [
        url.strip()
        for url in (
            item.find(name="loc").string for item in soup.find_all(name="sitemap")
        )
    ]

    return sitemaps


@task(name="Collects Sitemap Property URLs")
def collect_property_urls(html_bytes: bytes) -> list[Property]:
    """
    Parses HTML and collects property URLs

    Args:
        html_bytes: Incoming sitemap directory html bytes

    Returns:
        sitemaps: list of property urls

    """
    soup = BeautifulSoup(html_bytes, "html.parser")

    parsed_prop_urls: list[dict] = [
        {
            "property_url": item.find(name="loc").string.strip(),
            "last_modified": item.find(name="lastmod").string.strip(),
        }
        for item in soup.find_all(name="url")
    ]
    property_set: PropertySet = PropertySet.model_validate(
        parsed_prop_urls
    )  # Using here mainly to validate parsed fields

    return property_set.model_dump()


@task(
    description="Geneerates a CSRF Token from the site",
    retries=3,
    retry_delay_seconds=exponential_backoff(3),
    retry_jitter_factor=0.5,
)
def extract_csrf_token() -> str:
    """
    Generates a new csrf token
    """

    URL: str = "https://www.zillow.com/xml/indexes/us/hdp/for-sale-by-agent.xml.gz"

    headers = {"User-Agent": UserAgent().random}

    response: httpx.Response = httpx.get(URL, headers=headers)

    response.raise_for_status()

    csrf_token: str = response.headers["x-amz-cf-id"]

    return csrf_token


@task(
    description="Collects URLs from home detail site",
    retries=3,
    retry_delay_seconds=exponential_backoff(3),
    retry_jitter_factor=0.5,
)
def extract_sitemap_dir_urls() -> bytes:
    """
    Extracts property URLs from the ZIllow sitemap
    """
    URL: str = "https://www.zillow.com/xml/indexes/us/hdp/for-sale-by-agent.xml.gz"

    headers = {"User-Agent": UserAgent().random}

    response: httpx.Response = httpx.get(URL, headers=headers)

    response.raise_for_status()

    return response.content


@task(
    description="Collects URLs from home detail site",
    retries=3,
    retry_delay_seconds=exponential_backoff(3),
    retry_jitter_factor=0.5,
)
def extract_sitemap_urls(site_map_url: str) -> bytes:
    """
    Extracts property URLs from the ZIllow sitemap
    """

    headers = {"User-Agent": UserAgent().random}

    response: httpx.Response = httpx.get(site_map_url, headers=headers)

    response.raise_for_status()

    return response.content


@task(
    description="Collects Listing URL json",
    retries=3,
    retry_delay_seconds=exponential_backoff(5),
    retry_jitter_factor=0.5,
)
def extract_listing_url(property_url: str, csrf_token: str) -> bytes:
    """
    Extracts property URLs from the ZIllow sitemap
    """

    headers = {"User-Agent": UserAgent().random, "csrfToken": csrf_token}

    response: httpx.Response = httpx.Client().get(property_url, headers=headers)

    response.raise_for_status()

    return response.content
