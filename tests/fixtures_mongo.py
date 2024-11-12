"""
MongoDB Fixures
"""

from typing import Generator

import pytest
from mongomock import MongoClient

from zillow.sitemap_model import Property, PropertySet, ZillowRepository


@pytest.fixture(scope="session")
def mock_db() -> Generator[None, None, MongoClient]:
    """
    Creates a mock mongo db instance for local unit testing
    """

    with MongoClient() as c:
        yield c


@pytest.fixture(scope="session")
def property_set():

    return PropertySet(
        [
            Property(
                property_url="https://www.zillow.com/homedetails/9510-Amherst-Ave-APT-121-Margate-City-NJ-08402/2146997656_zpid/",
                last_modified="2024-08-14T14:53:00Z",
            ),
            Property(
                property_url="https://www.zillow.com/homedetails/20201-E-Country-Club-Dr-Aventura-FL-33180/2146995561_zpid/",
                last_modified="2024-08-13T04:19:00Z",
            ),
            Property(
                property_url="https://www.zillow.com/homedetails/2632-NW-18th-Ter-Oakland-Park-FL-33311/2146994027_zpid/",
                last_modified="2024-11-05T23:48:00Z",
            ),
        ]
    )


@pytest.fixture(scope="session")
def populate_mongo(mock_db, property_set):
    repo = ZillowRepository(mock_db["local"])

    repo.save_many(property_set)

    yield
