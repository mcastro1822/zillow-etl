"""
Tests queries
"""

import polars as pl
import pytest
import respx
from polars.testing import assert_frame_equal

from zillow.mongo_models.query_config import RegionConfig
from zillow.query import Payload, parse_max_pages, parse_result_content


@pytest.fixture
def region_config():
    raw_config = {
        "mapBounds": {
            "west": -118.668176,
            "east": -118.155289,
            "south": 33.703652,
            "north": 34.337306,
        },
        "usersSearchTerm": "Los Angeles, CA",
        "regionSelection": [{"regionId": 12447, "regionType": 6}],
        "filterState": {"sortSelection": {"value": "globalrelevanceex"}},
    }
    return RegionConfig.model_validate(raw_config)


class TestPayload:

    def test_from_config(self, region_config):
        """
        Verifies proper payload
        """
        payload: Payload = Payload.from_config(region_config, 2)

        assert payload.searchQueryState.pagination == {"currentPage": 2}
        assert payload.wants == {"cat1": ["listResults"], "cat2": ["total"]}


def test_query_search(respx_mock: respx.MockRouter):
    ...
    # query_search()


@pytest.mark.parametrize(
    "grab_json",
    [
        ("first_page.json"),
    ],
    indirect=True,
)
def test_parse_max_pages(grab_json):
    """
    Tests json to df function
    """
    pages_list = parse_max_pages.fn(grab_json)

    assert pages_list == [2, 3]


@pytest.mark.parametrize(
    "grab_json, grab_parquet",
    [
        ("first_page.json", "parsed_page.parquet"),
    ],
    indirect=True,
)
def test_parse_result_content(grab_json, grab_parquet):
    """
    Tests json to df function
    """
    df: pl.DataFrame = parse_result_content.fn(grab_json)

    assert_frame_equal(df, grab_parquet)
