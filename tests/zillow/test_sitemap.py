"""
Contains Tests for the Sitemap extractions
"""

from typing import Callable

import pytest
import respx
from httpx import Headers, Response

from zillow.sitemap import (
    collect_sitemap_indexes,
    extract_csrf_token,
    extract_sitemap_dir_urls,
    extract_sitemap_urls,
)


class TestSitemap:
    """
    Collection of Sitemap mapping tests
    """

    @pytest.mark.parametrize(
        "grab_html, func, url, param",
        [
            (
                "sitemap-index.html",
                extract_sitemap_dir_urls,
                "https://www.zillow.com/xml/indexes/us/hdp/for-sale-by-agent.xml.gz",
                False,
            ),
            (
                "sitemap.html",
                extract_sitemap_urls,
                "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0000.xml.gz",
                True,
            ),
        ],
        indirect=["grab_html"],
    )
    def test_extract_sitemap_dir_urls(
        self,
        grab_html: bytes,
        func: Callable,
        url: str,
        respx_mock: respx.MockRouter,
        param: bool,
    ):

        respx_mock.get(url).mock(return_value=Response(204, content=grab_html))

        content: bytes = func.fn() if param is False else func.fn(url)

        assert content == grab_html

    @pytest.mark.parametrize("grab_html", [("listing.html")], indirect=True)
    def test_extract_csrf_token(self, grab_html: bytes, respx_mock: respx.MockRouter):
        """
        Checks the csrf token is parsed
        """

        headers = Headers(
            {
                "content-type": "text/xml",
                "content-length": "287",
                "connection": "keep-alive",
                "last-modified": "Thu, 07 Nov 2024 08:01:27 GMT",
                "x-amz-server-side-encryption": "AES256",
                "content-encoding": "gzip",
                "accept-ranges": "bytes",
                "server": "AmazonS3",
                "date": "Fri, 08 Nov 2024 02:35:28 GMT",
                "etag": '"4aafc4776168134133742e4a63fd788b"',
                "vary": "accept-encoding",
                "x-cache": "RefreshHit from cloudfront",
                "via": "1.1 6261076d910bd4aa39084fae9b6733ee.cloudfront.net (CloudFront)",
                "x-amz-cf-pop": "JFK52-P7",
                "x-amz-cf-id": "P8lpdQBK8EmdB3k5MLUPbxJDSxws5vJY6JGOm_Bds3n4d872HnMmJA==",
            }
        )

        respx_mock.get(
            "https://www.zillow.com/xml/indexes/us/hdp/for-sale-by-agent.xml.gz"
        ).mock(return_value=Response(204, content=grab_html)).respond(headers=headers)
        csrf_token: str = extract_csrf_token.fn()
        assert csrf_token == "P8lpdQBK8EmdB3k5MLUPbxJDSxws5vJY6JGOm_Bds3n4d872HnMmJA=="

    @pytest.mark.parametrize(
        "grab_html",
        [("sitemap-index.html")],
        indirect=True,
    )
    def test_collect_sitemap_indexes(self, grab_html: bytes):

        sitemaps: list = collect_sitemap_indexes.fn(grab_html)

        assert sitemaps == [
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/latest.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0000.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0001.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0002.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0003.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0004.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0005.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0006.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0007.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0008.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0009.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0010.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0011.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0012.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0013.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0014.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0015.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0016.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0017.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0018.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0019.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0020.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0021.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0022.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0023.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0024.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0025.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0026.xml.gz",
            "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0027.xml.gz",
        ]
