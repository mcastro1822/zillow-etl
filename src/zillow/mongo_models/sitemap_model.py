"""
Module for MongoDB Sitemap module. Because each url has a last modified date we aim to
only extract urls which are different from the last modified date for each document
"""

import re
from functools import cached_property

from pendulum.datetime import DateTime
from pydantic import (
    Field,
    computed_field,
    field_validator,
)
from pydantic.networks import HttpUrl

from zillow.mongo_models.db import AbstractRepo, BaseDocument, DocumentSet


class Property(BaseDocument):
    """
    Property Document Base Model
    """

    property_url: str = Field(
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

        match: re.Match = re.search(REGEX_PATTERN, self.property_url)

        if match:
            return match.group(1)
        else:
            raise ValueError("No Zillow ID found. URL Erroneous")

    @field_validator("property_url")
    def validate_property_url(cls, value: str):
        """
        Simple Assertion to ensure the URLs are to zillow.com
        """

        url: HttpUrl = HttpUrl(value)
        assert url.host == "www.zillow.com"
        return value

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


class PropertySet(DocumentSet):
    """
    Property Set Model for collection
    """

    root: list[Property]


class ZillowRepository(AbstractRepo(Property, PropertySet, "product_zillow")):
    """
    Zillow Repository Model
    """

    def find_by_zid(self, zid: str) -> Property:
        """
        Finds document by zillow id
        """

        return self.find_one_by({"zillow_id": zid})
