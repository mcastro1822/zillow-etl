"""
Module for listing transformations
"""

from pydantic import BaseModel, Field


class Property(BaseModel):
    """
    Zillow Property Model
    """

    zpid: str = Field(
        name="Zillow Property id",
        description="The zillow id of the property",
        examples=[2146993218],
    )
    city: str = Field(
        name="City",
        description="City that the property resides in",
        examples=["Sandy Springs"],
    )
    state: str = Field(
        name="State", description="State that the property is in", examples=["CA", "GA"]
    )
    homeStatus: str = Field(
        name="Home Status",
        description="Home status of the property",
        examples=["FOR_SALE"],
    )

    address: dict = Field(
        name="Address",
        description="Property Address",
        examples=[
            {
                "streetAddress": "6851 Roswell Rd APT O31",
                "city": "Sandy Springs",
                "state": "GA",
                "zipcode": "30328",
                "neighborhood": None,
                "community": None,
                "subdivision": None,
            },
        ],
    )

    bedrooms: int = Field(
        name="Bedrooms",
        description="Number of bedrooms in the property",
        examples=[1, 2],
    )
    bathrooms: int = Field(
        name="Bathrooms",
        description="Number of bathrooms in the property",
        examples=[0, 1],
    )
    price: int = Field(
        name="Price", description="Price of the property", examples=[265000]
    )
    yearBuilt: int = Field(
        name="Year Built",
        description="Year the property was built",
        examples=[2000, 1964],
    )
    listing_sub_type: dict = Field(
        name="Listing Sub Type",
        description="Additional Categorical information",
        examples=[{"is_forAuction": False, "is_newHome": False}],
    )
    country: str = Field(
        name="Country", description="Country the property is in", examples=["USA"]
    )
    county: str = Field(
        name="County",
        description="County the property is in",
        examples=["Fulton County"],
    )
    homeType: str = Field(
        name="Home Type", description="Property Type", examples=["CONDO"]
    )
    currency: str = Field(name="Currency", description="Currency", examples=["USD"])
    resoFacts: dict = Field(
        name="Rest of Facts", description="Additional facts about the property"
    )
