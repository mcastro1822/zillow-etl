"""
Module for MongoDB Sitemap module. Because each url has a last modified date we aim to
only extract urls which are different from the last modified date for each document
"""

import re
from functools import cached_property

from pendulum import parse
from pendulum.datetime import DateTime
from pydantic import (
    BaseModel,
    Field,
    RootModel,
    computed_field,
    field_serializer,
    field_validator,
)
from pydantic.networks import HttpUrl, UrlConstraints
from pydantic_mongo import AbstractRepository, ObjectIdField
from typing_extensions import Annotated


class Property(BaseModel):
    """
    Property Document Base Model
    """

    id: ObjectIdField | None = Field(
        title="Document ID", description="MongoDB ID of the document", default=None
    )
    property_url: Annotated[
        HttpUrl, UrlConstraints(allowed_schemes=["https"], default_host="zillow.com")
    ] = Field(
        title="URL to Zillow Property",
        description="Static Zillow URL for a listing",
        exampes=[
            "https://www.zillow.com/homedetails/9510-Amherst-Ave-APT-121-Margate-City-NJ-08402/2146997656_zpid/"
        ],
    )
    last_modified: str = Field(
        name="Last Modified Date",
        description="Last Modified Date of the Zillow Property Listing",
        examples=["2024-08-14T14:53:00Z"],
    )

    @computed_field(return_type=str)
    @cached_property
    def zillow_id(self):
        """
        Zillow ID parsed from the URL listing
        """
        REGEX_PATTERN = "\/([0-9]+)[_]zpid\/"

        match: re.Match = re.search(REGEX_PATTERN, self.property_url.unicode_string())

        if match:
            return match.group(1)
        else:
            raise ValueError("No Zillow ID found. URL Erroneous")

    @field_validator("last_modified")
    @classmethod
    def validate_last_modified(cls, value: str) -> DateTime:
        """
        Last modified needs to be validated as a pendulum datetime instance
        """
        REGEX_PATTERN = "\d{4}[-]\d{2}[-]\d{2}T\d{2}\:\d{2}\:\d{2}Z"

        matched: re.Match = re.match(REGEX_PATTERN, value)
        if matched:
            date_string = matched.group(0)
            return date_string
        else:
            raise ValueError("No DateTime String could be parsed")

    @field_serializer("last_modified")
    def serialze_last_modified(self, value):

        dt = parse(value, exact=True)
        return dt


class PropertySet(RootModel):
    """
    Property Set Model for collection
    """

    root: list[Property]


class ZillowRepository(AbstractRepository[Property]):
    """
    Zillow Repository Model
    """

    class Meta:
        collection: str = "product_zillow"

    def find_by_zid(self, zid: str) -> list[Property]:
        """
        Finds document by zillow id
        """

        return list(self.find_by({"zillow_id": zid}))
