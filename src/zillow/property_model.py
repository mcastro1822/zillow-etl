"""
Module for listing transformations
"""

from pydantic import BaseModel, ConfigDict, Field


class Address(BaseModel):
    """
    Address Base Model
    """

    model_config = ConfigDict(extra="ignore")

    streetAddress: str = Field(
        name="Street Address", examples=["6851 Roswell Rd APT O31"]
    )
    city: str = Field(
        name="City",
        description="City that the property resides in",
        examples=["Sandy Springs"],
    )
    state: str = Field(
        name="State", description="State that the property is in", examples=["CA", "GA"]
    )
    zipcode: str = Field(
        name="Zip Code", description="Property Zip Code", examples=["30328"]
    )
    neighborhood: str | None = Field(name="Neighborhood")
    community: str | None = Field(name="Community")
    subdivision: str | None = Field(name="Subdivision")


class ResoFacts(BaseModel):
    """
    Property Rest of Facts Base Model
    """

    model_config = ConfigDict(extra="ignore")

    architecturalStyle: str = Field(
        name="Architectural Style",
        description="Style of the property",
        examples=["European,Traditional"],
    )
    appliances: list = Field(
        name="Appliamces",
        description="List of appliances for the property",
        examples=[
            [
                "Dishwasher",
                "Disposal",
            ]
        ],
    )
    communityFeatures: list = Field(
        name="Community Features",
        description="List of community features for the property",
        examples=[
            [
                "Clubhouse",
                "Homeowners Assoc",
            ]
        ],
    )
    hasCooling: bool = Field(
        name="Has Cooling",
        description="Boolean indicator for whether a property has cooling",
        examples=[True, False],
    )
    hasHeating: bool = Field(
        name="Has Heating",
        description="Boolean indicator for whether a property has heating",
        examples=[True, False],
    )
    taxAnnualAmount: int = Field(
        name="Tax Annual Amount",
        description="Annual tax amount of the proeprty",
        examples=[1287],
    )
    stories: int = Field(
        name="Stories", description="Number of floors a property has", examples=[1, 2]
    )


class Property(BaseModel):
    """
    Zillow Property Model
    """

    model_config = ConfigDict(extra="ignore")

    zpid: int = Field(
        name="Zillow Property id",
        description="The zillow id of the property",
        examples=[2146993218],
    )

    homeStatus: str = Field(
        name="Home Status",
        description="Home status of the property",
        examples=["FOR_SALE"],
    )

    address: Address = Field(
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
    resoFacts: ResoFacts = Field(
        name="Rest of Facts", description="Additional facts about the property"
    )
    monthlyHoaFee: int = Field(name="Monthly HOA Fee", examples=[486])
    livingArea: int = Field(
        name="Living Area", description="Living Area Size", examples=[1206]
    )
    livingAreaUnits: str = Field(
        name="Living Area Units",
        description="Living Area Units",
        examples=["Square Feet"],
    )
    zestimate: int = Field(
        name="Zestimate", description="Zillow Price Estimate", examples=[262100]
    )
    rentZestimate: int = Field(
        name="Rent Zestimate", description="Zillow Rent Estimate", examples=[2114]
    )
    latitude: float = Field(name="Latitude", examples=[33.94186])
    longitude: float = Field(name="Longitude", examples=[-84.37228])
    brokerageName: str = Field(
        name="Brokerage Name", examples=["Presley Roth Real Estate"]
    )
    propertyTaxRate: float = Field(name="Property Tax Rate", examples=[0.82])
    mlsid: str = Field(
        name="MLS ID",
        description="Unique Identifier across platforms for the listing",
        examples=["7477717"],
    )
