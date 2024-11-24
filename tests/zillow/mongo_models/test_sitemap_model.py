"""
Module for testing mongo db property configs
"""

import pytest

from zillow.mongo_models.sitemap_model import Property, ZillowRepository


class TestProperty:

    @pytest.mark.parametrize(
        "last_modified,  is_valid_date",
        [
            ("2024-11-05T23:48:00Z", True),
            ("2024-a-05", False),
            ("32-334-XX", False),
        ],
    )
    def test_last_modified(self, last_modified, is_valid_date):
        if is_valid_date is True:

            Property.validate_last_modified(last_modified)

        if is_valid_date is False:
            with pytest.raises(ValueError):

                Property.validate_last_modified(last_modified)

    @pytest.mark.parametrize(
        "property_url, last_modified, expected_zid",
        [
            (
                "https://www.zillow.com/homedetails/2632-NW-18th-Ter-Oakland-Park-FL-33311/2146994027_zpid/",
                "2024-11-05T23:48:00Z",
                "2146994027",
            ),
            (
                "https://www.zillow.com/homedetails/20201-E-Country-Club-Dr-Aventura-FL-33180/2146995561_zpid/",
                "2024-08-13T04:19:00Z",
                "2146995561",
            ),
        ],
    )
    def test_expected_zid(self, property_url, last_modified, expected_zid):
        """
        Checks that the proper zillow id was parsed
        """
        property = Property(property_url=property_url, last_modified=last_modified)

        assert property.zillow_id == expected_zid


class TestZillowRepository:

    def test_find_by_zid(self, mock_db, populate_mongo):

        repo = ZillowRepository(mock_db["production"])

        property: Property = repo.find_by_zid("2146997656")

        assert (
            property.property_url
            == "https://www.zillow.com/homedetails/9510-Amherst-Ave-APT-121-Margate-City-NJ-08402/2146997656_zpid/"
        )
        assert property.last_modified == "2024-08-14T14:53:00Z"
        assert property.zillow_id == "2146997656"
