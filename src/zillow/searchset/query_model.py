"""
Model for Result set
"""

from pydantic import BaseModel, ConfigDict, Field


class ResultSet(BaseModel):
    """
    Set of daily fields to parse
    """

    model_config = ConfigDict(extra="ignore")

    zpid: int = Field(
        name="Zillow Property id",
        description="The zillow id of the property",
        examples=[2146993218],
    )
    unformattedPrice: int = Field(
        name="Unformatted Price", description="Price of the property", examples=[265000]
    )
