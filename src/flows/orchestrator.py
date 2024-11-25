from functools import reduce

import polars as pl
from prefect import flow, task

from flows.pull_listing import query_zillow_listings
from flows.utility import batch_task_results
from zillow.blocks import blocks
from zillow.mongo_models.sitemap_model import Property, ZillowRepository
from zillow.sitemap import (
    collect_property_urls,
    collect_sitemap_indexes,
    extract_sitemap_dir_urls,
    extract_sitemap_urls,
)


@task(description="Checks against the MongoDB for newly modified Urls")
def return_recently_modified(sitemap_results: list[Property]) -> list[dict]:
    """ """

    repo = ZillowRepository((blocks.mongodb).get_client()["production"])

    current_props: list[dict] = repo.get_all().model_dump()

    current_df: pl.DataFrame = pl.from_dicts(current_props).drop("id")

    sitemap_df: pl.DataFrame = pl.from_dicts(sitemap_results).drop("id")

    df = (
        sitemap_df.join(
            current_df, on=["property_url", "zillow_id"], how="left", suffix="_current"
        )
        .filter(
            (
                pl.col("last_modified").cast(pl.Datetime)
                > pl.col("last_modified_current").cast(pl.Datetime)
            )
            | (pl.col("last_modified_current").is_null())
        )
        .drop("last_modified_current")
    )

    return df.to_dicts()


@flow(name="Queue Zillow Property Listings")
def queue_listings(state_code: str):
    """
    Queues listings to scrape via state

    Args:
        state_code: Two character state abbreviation to supply


    """
    sitemap_dir_html: bytes = extract_sitemap_dir_urls()

    sitemap_indexes: list = collect_sitemap_indexes(sitemap_dir_html)
    sitemap_indexes = sitemap_indexes[1:2]
    results: list[list[Property]] = reduce(
        lambda output, func: batch_task_results(func, output),
        [extract_sitemap_urls, collect_property_urls],
        sitemap_indexes,
    )  # Tried unnesting this in the lower layer, didnt work, gave up and moved on oh well

    results: list[dict] = [
        result for nested_result in results for result in nested_result
    ]

    query_zillow_listings(results)
    properties_to_queue: dict = return_recently_modified(results)

    """
    Need to add in worker deployment here as well as refresh rate for csrf token
    """

    return properties_to_queue
