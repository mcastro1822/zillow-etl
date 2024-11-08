"""
Module for collecting listings from Zillow Sitemap
"""

import httpx
from getuseragent import UserAgent
from prefect import task


@task(description="Geneerates a CSRF Token from the site")
def extract_csrf_token():
    """
    Generates a new csrf token
    """

    URL: str = "https://www.zillow.com/xml/indexes/us/hdp/for-sale-by-agent.xml.gz"

    headers = {"User-Agent": UserAgent().Random()}

    response: httpx.Response = httpx.get(URL, headers=headers)

    response.raise_for_status()

    csrf_token: str = response.headers["x-amz-cf-id"]
    print(response.headers)
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
