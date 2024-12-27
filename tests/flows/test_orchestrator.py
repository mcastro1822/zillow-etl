import random

import polars as pl
import pytest
import respx
from httpx import Headers, Response
from polars.testing import assert_frame_equal
from pytest import MonkeyPatch

from flows.attributes import queue_listings_attributes
from flows.utility import return_recently_modified


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
def sitemap_html_bytes_0000():
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
            2024-09-13T04:19:00Z
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


@pytest.fixture
def sitemap_html_bytes_0001():
    html_string: str = """
        <?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <url>
            <loc>
            https://www.zillow.com/homedetails/240-Brooks-St-SE-UNIT-E201-Fort-Walton-Beach-FL-32548/2146955997_zpid/
            </loc>
            <lastmod>
            2024-09-14T17:46:00Z
            </lastmod>
            </url>
            <url>
            <loc>
            https://www.zillow.com/homedetails/2529-W-Warren-Blvd-Chicago-IL-60612/2146954801_zpid/
            </loc>
            <lastmod>
            2024-09-25T16:25:00Z
            </lastmod>
            </url>
            <url>
            <loc>
            https://www.zillow.com/homedetails/7205-Thomas-Dr-UNIT-E2003-Panama-City-Beach-FL-32408/2146954389_zpid/
            </loc>
            <lastmod>
            2024-06-25T17:43:00Z
            </lastmod>
        </urlset>
        """
    return bytes(html_string, encoding="utf-8")


@pytest.fixture
def mock_sitemap_results():
    results = [
        {
            "id": None,
            "property_url": "https://www.zillow.com/homedetails/9510-Amherst-Ave-APT-121-Margate-City-NJ-08402/2146997656_zpid/",
            "last_modified": "2024-08-14T14:53:00Z",
            "zillow_id": "2146997656",
        },
        {
            "id": None,
            "property_url": "https://www.zillow.com/homedetails/20201-E-Country-Club-Dr-Aventura-FL-33180/2146995561_zpid/",
            "last_modified": "2024-09-13T04:19:00Z",
            "zillow_id": "2146995561",
        },
        {
            "id": None,
            "property_url": "https://www.zillow.com/homedetails/2632-NW-18th-Ter-Oakland-Park-FL-33311/2146994027_zpid/",
            "last_modified": "2024-11-05T23:48:00Z",
            "zillow_id": "2146994027",
        },
        {
            "id": None,
            "property_url": "https://www.zillow.com/homedetails/9155-Nesbit-Ferry-Rd-UNIT-49-Alpharetta-GA-30022/2146985037_zpid/",
            "last_modified": "2024-09-13T14:00:00Z",
            "zillow_id": "2146985037",
        },
    ]

    return results


def test_return_recently_modified(
    prefect_test_fixture,
    populate_prefect_blocks,
    mock_sitemap_results,
    mock_db,
    populate_mongo,
    monkeypatch: MonkeyPatch,
):
    """
    Ensures retrieval of desired URLs
    """
    monkeypatch.setattr("flows.utility.blocks.mongodb.get_client", lambda: mock_db)

    new_or_recently_modified = return_recently_modified.fn(mock_sitemap_results)

    assert new_or_recently_modified.to_dicts() == [
        {
            "property_url": "https://www.zillow.com/homedetails/20201-E-Country-Club-Dr-Aventura-FL-33180/2146995561_zpid/",
            "last_modified": "2024-09-13T04:19:00Z",
            "zillow_id": "2146995561",
        },
        {
            "property_url": "https://www.zillow.com/homedetails/9155-Nesbit-Ferry-Rd-UNIT-49-Alpharetta-GA-30022/2146985037_zpid/",
            "last_modified": "2024-09-13T14:00:00Z",
            "zillow_id": "2146985037",
        },
    ]


@pytest.mark.parametrize(
    "grab_html, grab_parquet",
    [("listing.html", "property.parquet")],
    indirect=True,
)
@respx.mock(assert_all_mocked=True)
def test_orchestrator(
    sitemap_index_html_bytes: bytes,
    sitemap_html_bytes_0000: bytes,
    sitemap_html_bytes_0001: bytes,
    prefect_test_fixture,
    populate_prefect_blocks,
    mock_db,
    populate_mongo,
    respx_mock: respx.MockRouter,
    monkeypatch: MonkeyPatch,
    grab_html,
    grab_parquet,
):

    headers = Headers(
        headers={
            "x-amz-cf-id": "P8lpdQBK8EmdB3k5MLUPbxJDSxws5vJY6JGOm_Bds3n4d872HnMmJA==",
        },
        encoding="utf-8",
    )

    respx_mock.get(
        "https://www.zillow.com/xml/indexes/us/hdp/for-sale-by-agent.xml.gz"
    ).mock(
        return_value=Response(204, content=sitemap_index_html_bytes, headers=headers)
    )
    respx_mock.get(
        "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0000.xml.gz"
    ).mock(return_value=Response(204, content=sitemap_html_bytes_0000))

    respx_mock.get(
        "https://www.zillow.com/xml/sitemaps/us/hdp/for-sale-by-agent/sitemap-0001.xml.gz"
    ).mock(return_value=Response(204, content=sitemap_html_bytes_0001))

    monkeypatch.setattr(random, "randint", lambda x, y: 1)

    respx_mock.get(url__startswith="https://www.zillow.com/homedetails/").mock(
        return_value=Response(204, content=grab_html)
    )

    df: pl.DataFrame = queue_listings_attributes().unique()

    assert_frame_equal(df, grab_parquet)
