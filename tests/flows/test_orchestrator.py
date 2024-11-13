import pytest
import respx
from httpx import Response
from pytest import MonkeyPatch

from flows.orchestrator import queue_listings


@pytest.fixture
def sitemap_index_html_bytes():
    html_string: str = """
        <?xml version="1.0" encoding="UTF-8"?>
        <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <sitemap>
            <loc>
            https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0000.xml.gz
            </loc>
            </sitemap>
            <sitemap>
            <loc>
            https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0001.xml.gz
            </loc>
            </sitemap>
        </sitemapindex>
        """
    return bytes(html_string, encoding="utf-8")


@pytest.fixture
def sitemap_html_bytes():
    html_string: str = """
        <?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <url>
            <loc>
            https://www.zillow.com/homedetails/9510-Amherst-Ave-APT-121-Margate-City-NJ-08402/2146997656_zpid/
            </loc>
            <lastmod>
            2024-08-14T14:53:00Z
            </lastmod>
            </url>
            <url>
            <loc>
            https://www.zillow.com/homedetails/20201-E-Country-Club-Dr-Aventura-FL-33180/2146995561_zpid/
            </loc>
            <lastmod>
            2024-08-13T04:19:00Z
            </lastmod>
            </url>
            <url>
            <loc>
            https://www.zillow.com/homedetails/2632-NW-18th-Ter-Oakland-Park-FL-33311/2146994027_zpid/
            </loc>
            <lastmod>
            2024-11-05T23:48:00Z
            </lastmod>
            </url>
        </urlset>
        """
    return bytes(html_string, encoding="utf-8")


def test_orchestrator(
    sitemap_index_html_bytes: bytes,
    sitemap_html_bytes: bytes,
    prefect_test_fixture,
    mock_db,
    respx_mock: respx.MockRouter,
    monkey_patch: MonkeyPatch,
):

    respx_mock.get(
        "https://www.zillow.com/xml/indexes/us/hdp/for-sale-by-agent.xml.gz"
    ).mock(return_value=Response(204, content=sitemap_index_html_bytes))
    respx_mock.get(
        "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0000.xml.gz"
    ).mock(return_value=Response(204, content=sitemap_html_bytes))
    respx_mock.get(
        "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0001.xml.gz"
    ).mock(return_value=Response(204, content=sitemap_html_bytes))
    monkey_patch.setattr(
        "zillow.recently_modified.blocks.mongodb.get_client", lambda: mock_db
    )
    queue_listings("CA")

    assert False
