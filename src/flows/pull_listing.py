"""
Worker Flow to pull and transform zillow listing
"""

import random
import time

import polars as pl
from prefect import flow, task, unmapped
from prefect.futures import PrefectFuture
from prefecto.concurrency import BatchTask

from flows.utility import modify_param_on_retry
from zillow.extract.listing import collect_listing_attrs
from zillow.mongo_models.sitemap_model import Property
from zillow.sitemap import extract_csrf_token, extract_listing_url
from zillow.transform.listing import property_json_to_df


@task(name="Collect Listing", description="Collects Listing Datafram")
def listing_collection(property_dict: dict, csrf_token: str) -> pl.DataFrame:
    """
    Handles request, json parse from html, and converstion to dataframe

    Args:
        property_url: URL of the listing
        csrf_token: Token for use across each worker node

    Returns:
        df: Dataframe for the listing
    """
    sleep_time: int = random.randint(50, 150)
    time.sleep(sleep_time)

    csrf_token = modify_param_on_retry(csrf_token)

    properties: Property = Property.model_validate(property_dict)

    html_bytes: bytes = extract_listing_url.submit(
        properties.property_url, csrf_token
    ).result()
    listing_json: dict = collect_listing_attrs.submit(html_bytes).result()
    df: pl.DataFrame = property_json_to_df.submit(listing_json).result()

    return df


@flow(name="Query Zillow Listing", description="Collects listing data")
def query_zillow_listings(property_urls: list[dict]):
    """
    Queries Zillow to extract listing json.
    """
    csrf_token = extract_csrf_token()

    batch_get = BatchTask(listing_collection, 60)

    futures: list[PrefectFuture] = batch_get.map(property_urls, unmapped(csrf_token))

    results: list = [future.result() for future in futures]

    df: pl.DataFrame = pl.concat(results, how="diagonal_relaxed")

    return df
