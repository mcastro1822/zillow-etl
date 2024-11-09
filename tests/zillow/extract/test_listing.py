"""
Module to test extracting json from listings 
"""

import pytest

from zillow.extract.listing import collect_listing_attrs


class TestListings:

    @pytest.mark.parametrize(
        "grab_html, grab_json",
        [
            ("listing.html", "listing.json"),
        ],
        indirect=True,
    )
    def test_collect_listing_attrs(self, grab_html: bytes, grab_json: dict):
        results = collect_listing_attrs.fn(grab_html)
        assert results == grab_json
