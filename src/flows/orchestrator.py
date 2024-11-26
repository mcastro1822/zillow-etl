from functools import reduce

from prefect import flow

from flows.pull_listing import query_zillow_listings
from flows.queryset import query_zillow_regions
from flows.utility import batch_task_results, return_recently_modified
from zillow.blocks import blocks
from zillow.mongo_models.query_config import RegionDefinitionsRepo
from zillow.mongo_models.sitemap_model import Property
from zillow.sitemap import (
    collect_property_urls,
    collect_sitemap_indexes,
    extract_sitemap_dir_urls,
    extract_sitemap_urls,
)


@flow(name="Queue Zillow Property Listing Attributes")
def queue_listings_attributes():
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

    query_zillow_listings(results)
    # properties_to_queue: dict = return_recently_modified(results)

    """
    Need to add in worker deployment here as well as refresh rate for csrf token
    """

    # return properties_to_queue


@flow(name="Queue Zillow Property Listings")
def queue_listings():
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

    config_repo = RegionDefinitionsRepo((blocks.mongodb).get_client()["production"])

    configs = config_repo.get_all()

    recently_modified = return_recently_modified(results)

    for region_config in configs:
        query_zillow_regions(region_config, recently_modified)

    """
    Need to add in worker deployment here as well as refresh rate for csrf token
    """

    return None
