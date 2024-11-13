import pytest
from polars.testing import assert_frame_equal

from zillow.transform.listing import property_json_to_df


@pytest.mark.parametrize(
    "grab_json, grab_parquet",
    [("listing.json", "property.parquet")],
    indirect=True,
)
def test_property_json_to_df(grab_json, grab_parquet):
    """
    Tests json to df transform
    """
    results = property_json_to_df.fn(grab_json)
    assert_frame_equal(results, grab_parquet)
