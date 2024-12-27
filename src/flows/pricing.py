"""
Daily Pricing Query
"""

from prefect import flow

from flows.queryset import query_zillow_regions
from zillow.blocks import blocks
from zillow.mongo_models.query_config import RegionDefinitionsRepo


@flow(name="Queue Zillow Property Listings")
def queue_prices():
    """
    Queues listings to scrape via state

    Args:
        state_code: Two character state abbreviation to supply


    """

    config_repo = RegionDefinitionsRepo((blocks.mongodb).get_client()["production"])

    configs = config_repo.get_all().root

    for region_config in configs:
        query_zillow_regions(region_config)

    """
    Need to add in worker deployment here as well as refresh rate for csrf token
    """

    return None
