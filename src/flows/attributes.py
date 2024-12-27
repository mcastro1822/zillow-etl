"""
Monthly Attributes Run
"""

from functools import reduce

import polars as pl
from prefect import flow

from flows.pull_listing import query_zillow_listings
from flows.utility import batch_task_results
from zillow.mongo_models.sitemap_model import Property
from zillow.sitemap import (
    collect_property_urls,
    collect_sitemap_indexes,
    extract_sitemap_dir_urls,
    extract_sitemap_urls,
)


@flow(name="Queue Zillow Property Listing Attributes")
def queue_listings_attributes() -> pl.DataFrame:
    """
    Queues listings to scrape individual property attributes


    """
    sitemap_dir_html: bytes = extract_sitemap_dir_urls()

    sitemap_indexes: list = collect_sitemap_indexes(sitemap_dir_html)

    results: list[list[Property]] = reduce(
        lambda output, func: batch_task_results(func, output),
        [extract_sitemap_urls, collect_property_urls],
        sitemap_indexes,
    )  # Tried unnesting this in the lower layer, didnt work, gave up and moved on oh well

    results: list[dict] = [
        result for nested_result in results for result in nested_result
    ]

    df = query_zillow_listings(results)
    # properties_to_queue: dict = return_recently_modified(results)

    """
    Need to add in worker deployment here as well as refresh rate for csrf token
    """

    return df
