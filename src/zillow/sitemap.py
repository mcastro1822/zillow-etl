"""
Module for collecting listings from Zillow Sitemap
"""

import httpx
from bs4 import BeautifulSoup
from getuseragent import UserAgent
from prefect import task

from zillow.sitemap_model import PropertySet


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
def collect_property_urls(html_bytes: bytes) -> list:
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
    property_set: PropertySet = PropertySet.model_validate(parsed_prop_urls)

    return property_set


@task(description="Geneerates a CSRF Token from the site")
def extract_csrf_token() -> str:
    """
    Generates a new csrf token
    """

    URL: str = "https://www.zillow.com/xml/indexes/us/hdp/for-sale-by-agent.xml.gz"

    headers = {"User-Agent": UserAgent().Random()}

    response: httpx.Response = httpx.get(URL, headers=headers)

    response.raise_for_status()

    csrf_token: str = response.headers["x-amz-cf-id"]

    return csrf_token


@task(description="Collects URLs from home detail site")
def extract_sitemap_dir_urls() -> bytes:
    """
    Extracts property URLs from the ZIllow sitemap
    """
    URL: str = "https://www.zillow.com/xml/indexes/us/hdp/for-sale-by-agent.xml.gz"

    headers = {"User-Agent": UserAgent().Random()}

    response: httpx.Response = httpx.get(URL, headers=headers)

    response.raise_for_status()

    return response.content


@task(description="Collects URLs from home detail site")
def extract_sitemap_urls(site_map_url: str) -> bytes:
    """
    Extracts property URLs from the ZIllow sitemap
    """

    headers = {"User-Agent": UserAgent().Random()}

    response: httpx.Response = httpx.get(site_map_url, headers=headers)

    response.raise_for_status()

    return response.content
