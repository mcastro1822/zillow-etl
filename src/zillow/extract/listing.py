"""
Module dealing with extraction of listing data
"""

import orjson
from bs4 import BeautifulSoup
from prefect import task


@task(description="Parses HTML file for listing JSON")
def collect_listing_attrs(html_bytes: bytes) -> dict:
    """
    Parses html file from a zillow listing and searches for the json attributes

    Args:
        html_bytes: html from requested zillow listing

    Returns:
        listing_json: Listing JSON containing its attributes

    """
    soup = BeautifulSoup(html_bytes, "html.parser")

    listing_raw: str = soup.find(
        name="script", attrs={"id": "__NEXT_DATA__", "type": "application/json"}
    ).contents

    assert len(listing_raw) == 1

    json_file: dict = orjson.loads(str(listing_raw[0]))

    raw_property_json: dict = orjson.loads(
        json_file["props"]["pageProps"]["componentProps"]["gdpClientCache"]
    )

    assert len(raw_property_json) == 1

    property_json = list(raw_property_json.values())[0]

    return property_json
