"""
Tests for Listings Transforms
"""

import pytest

from zillow.individual_property.property_model import Address, Property, ResoFacts


class TestModels:

    @pytest.mark.parametrize(
        "grab_json",
        [("listing.json")],
        indirect=True,
    )
    def test_address(self, grab_json: dict):

        address = grab_json["property"]["address"]
        model: Address = Address.model_validate(address)
        assert model == Address(
            streetAddress="6851 Roswell Rd APT O31",
            city="Sandy Springs",
            state="GA",
            zipcode="30328",
            neighborhood=None,
            community=None,
            subdivision=None,
        )

    @pytest.mark.parametrize(
        "grab_json",
        [("listing.json")],
        indirect=True,
    )
    def test_resofacts(self, grab_json: dict):
        rest_of_facts = grab_json["property"]["resoFacts"]
        model: ResoFacts = ResoFacts.model_validate(rest_of_facts)

        assert model.architecturalStyle == "European,Traditional"
        assert model.appliances == [
            "Dishwasher",
            "Disposal",
            "Dryer",
            "Gas Range",
            "Microwave",
            "Refrigerator",
            "Washer",
        ]
        assert model.communityFeatures == [
            "Clubhouse",
            "Homeowners Assoc",
            "Meeting Room",
            "Near Schools",
            "Near Shopping",
            "Pool",
            "Street Lights",
            "Tennis Court(s)",
        ]
        assert model.hasCooling is True
        assert model.hasHeating is True
        assert model.taxAnnualAmount == 1287
        assert model.stories == 1

    @pytest.mark.parametrize(
        "grab_json",
        [("listing.json")],
        indirect=True,
    )
    def test_property(self, grab_json: dict):
        prop = grab_json["property"]
        model = Property.model_validate(prop)

        assert model.zpid == 2146993218
        assert model.homeStatus == "FOR_SALE"
        assert model.bedrooms == 2
        assert model.bathrooms == 2
        assert model.price == 265000
        assert model.yearBuilt == 1964
        assert model.country == "USA"
        assert model.county == "Fulton County"
        assert model.homeType == "CONDO"
        assert model.currency == "USD"
        assert model.monthlyHoaFee == 486
        assert model.livingArea == 1206
        assert model.livingAreaUnits == "Square Feet"
        assert model.zestimate == 262100
        assert model.rentZestimate == 2114
        assert model.latitude == 33.94186
        assert model.longitude == -84.37228
        assert model.brokerageName == "Presley Roth Real Estate"
        assert model.propertyTaxRate == 0.82
        assert model.mlsid == "7477717"
