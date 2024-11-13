"""
Tests the worker node
"""

import pytest
import respx
from httpx import Headers, Response
from polars.testing import assert_frame_equal

from flows.pull_listing import query_zillow_listings


@pytest.mark.parametrize(
    "grab_html, grab_parquet",
    [("listing.html", "property.parquet")],
    indirect=True,
)
def test_query_zillow_listings(
    grab_html,
    grab_parquet,
    prefect_test_fixture,
    respx_mock: respx.MockRouter,
):

    property_urls: list[str] = [
        "https://www.zillow.com/homedetails/20201-E-Country-Club-Dr-Aventura-FL-33180/2146995561_zpid/"
    ]

    headers = Headers(
        {
            "x-amz-cf-id": "P8lpdQBK8EmdB3k5MLUPbxJDSxws5vJY6JGOm_Bds3n4d872HnMmJA==",
        }
    )

    respx_mock.get(
        "https://www.zillow.com/xml/indexes/us/hdp/for-sale-by-agent.xml.gz"
    ).mock(return_value=Response(204)).respond(headers=headers)

    respx_mock.get(property_urls[0]).mock(return_value=Response(204, content=grab_html))

    df = query_zillow_listings(property_urls)

    assert_frame_equal(df, grab_parquet)
