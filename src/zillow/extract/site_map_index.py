"""
Module for extraction of Sitemap URLs
"""

from bs4 import BeautifulSoup
from prefect import task


@task(name="Collects Sitemap partitions")
def collect_sitemap_partitions(html_bytes: bytes) -> list:
    """
    Parses HTML and converts partitions into a list

    Args:
        html_bytes: Incoming sitemap directory html bytes

    Returns:
        sitemaps: list of sitemap urls

    """
    soup = BeautifulSoup(html_bytes, "html.parser")
    soup
