"""
Worker Flow to pull and transform zillow listing
"""

import polars as pl
from prefect import flow, task, unmapped
from prefect.futures import PrefectFuture
from prefecto.concurrency import BatchTask

from zillow.extract.listing import collect_listing_attrs
from zillow.sitemap import extract_csrf_token, extract_listing_url
from zillow.transform.listing import property_json_to_df


@task(name="Collect Listing", description="Collects Listing Datafram")
def listing_collection(property_url: str, csrf_token: str) -> pl.DataFrame:
    """
    Handles request, json parse from html, and converstion to dataframe

    Args:
        property_url: URL of the listing
        csrf_token: Token for use across each worker node

    Returns:
        df: Dataframe for the listing
    """

    html_bytes: bytes = extract_listing_url.fn(property_url, csrf_token)
    listing_json: dict = collect_listing_attrs.fn(html_bytes)
    df: pl.DataFrame = property_json_to_df.fn(listing_json)

    return df


@flow(name="Query Zillow Listing", description="Collects listing data")
def query_zillow_listings(property_urls: list[str]):
    """
    Queries Zillow to extract listing json.
    """
    csrf_token = extract_csrf_token()

    batch_get = BatchTask(listing_collection, 10)

    futures: list[PrefectFuture] = batch_get.map(property_urls, unmapped(csrf_token))

    results: list = [future.result() for future in futures]

    return results
