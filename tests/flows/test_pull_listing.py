"""
Tests the worker node
"""

import random

import pytest
import respx
from httpx import Headers, Response
from polars.testing import assert_frame_equal
from pytest import MonkeyPatch

from flows.pull_listing import query_zillow_listings


@pytest.mark.parametrize(
    "grab_html, grab_parquet",
    [("listing.html", "property.parquet")],
    indirect=True,
)
@respx.mock(base_url="www.zillow.com")
def test_query_zillow_listings(
    grab_html,
    grab_parquet,
    prefect_test_fixture,
    respx_mock: respx.MockRouter,
    monkeypatch: MonkeyPatch,
):

    property_urls: list[str] = [
        {
            "property_url": "https://www.zillow.com/homedetails/20201-E-Country-Club-Dr-Aventura-FL-33180/2146995561_zpid/",
            "last_modified": "2024-08-14T14:53:00Z",
        }
    ]

    headers = Headers(
        {
            "x-amz-cf-id": "P8lpdQBK8EmdB3k5MLUPbxJDSxws5vJY6JGOm_Bds3n4d872HnMmJA==",
        }
    )

    respx_mock.get(
        "https://www.zillow.com/xml/indexes/us/hdp/for-sale-by-agent.xml.gz"
    ).mock(return_value=Response(204, headers=headers))

    respx_mock.get(property_urls[0].get("property_url")).mock(
        return_value=Response(204, content=grab_html)
    )

    monkeypatch.setattr(random, "randint", lambda x, y: 1)

    df = query_zillow_listings(property_urls)

    assert_frame_equal(df, grab_parquet)
